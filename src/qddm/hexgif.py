# SPDX-FileCopyrightText: 2026 Cecil-IA Labs
# SPDX-License-Identifier: MIT
#
# Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
# Organization: Cecil-IA Labs
# Project: Quad-Dimensional DataMatrix
#
# AI-assisted development:
# OpenAI ChatGPT and Codex were used as development tools.
# Human-directed development and integration.
# No OpenAI sponsorship, affiliation, or endorsement is implied.
#
# License: See the repository LICENSE file and SPDX identifier above.

"""Hexadecimal-only public values and an indexed-GIF research adapter.

The adapter records complete frames. It preserves the caller's palette order
and never quantizes or converts palette entries into a channel-vector API.
Payload length remains caller-supplied while framing is under discussion.
"""
from __future__ import annotations

import io
import math
import re
import struct
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from PIL import Image

TITLE = "Quad-Dimensional DataMatrix"
AUTHORS = ("João Paulo De Luca Jr", "Jorge Luiz Espanhol")
DEFAULT_PALETTE = tuple(f"#{(i * 0x9E3779) & 0xFFFFFF:06X}" for i in range(64))


@dataclass(frozen=True)
class Profile:
    pixel_side: int = 256
    module_side: int = 4
    effective_side: int = 64
    max_colors: int = 64
    max_frames: int = 64

    def __post_init__(self):
        if (self.pixel_side, self.module_side, self.effective_side,
                self.max_colors, self.max_frames) != (256, 4, 64, 64, 64):
            raise ValueError("This RfD prototype uses the 256/4/64 working profile")


PROFILE = Profile()


@dataclass(frozen=True)
class Frame:
    palette_hex: tuple[str, ...]
    delay_cs: int
    image_data: bytes
    interlaced: bool = False


@dataclass(frozen=True)
class Encoding:
    gif: bytes
    payload_bytes: int
    frame_count: int
    colors: int
    duration_ms: int


def _palette(values: Sequence[str]) -> tuple[str, ...]:
    result = tuple(values)
    if len(result) not in (2, 4, 8, 16, 32, 64):
        raise ValueError("Choose 2, 4, 8, 16, 32, or 64 hexadecimal entries")
    if any(not isinstance(v, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", v)
           for v in result):
        raise ValueError("Palette entries must be six-digit hexadecimal values")
    result = tuple(v.upper() for v in result)
    if len(set(result)) != len(result):
        raise ValueError("Palette entries must be distinct")
    return result


def _table_bytes(values: Sequence[str]) -> bytes:
    return bytes.fromhex("".join(v[1:] for v in _palette(values)))


def _payload(value: str) -> bytes:
    if not isinstance(value, str) or not re.fullmatch(r"(?:[0-9a-fA-F]{2})*", value):
        raise ValueError("Payload must contain complete hexadecimal octets")
    return bytes.fromhex(value)


def pack_dimensions(values: np.ndarray, bits: int) -> str:
    """Pack dimension identifiers in row-major order into hexadecimal octets."""
    values = np.asarray(values)
    if bits not in (1, 2, 3, 4, 5, 6) or values.dtype.kind not in "iu":
        raise ValueError("Expected integer dimensions with 1 to 6 bits each")
    if np.any(values < 0) or np.any(values >= 1 << bits):
        raise ValueError("Dimension is outside the active palette")
    binary = ((values.astype(np.uint16).reshape(-1, 1)
               >> np.arange(bits - 1, -1, -1)) & 1).astype(np.uint8)
    return np.packbits(binary, bitorder="big").tobytes().hex().upper()


def unpack_dimensions(payload_hex: str, bits: int, count: int) -> np.ndarray:
    if bits not in (1, 2, 3, 4, 5, 6) or count < 0:
        raise ValueError("Invalid dimension geometry")
    binary = np.unpackbits(np.frombuffer(_payload(payload_hex), np.uint8), bitorder="big")
    if len(binary) > count * bits:
        raise ValueError("Payload exceeds the requested dimension count")
    binary = np.pad(binary, (0, count * bits - len(binary)))
    weights = 1 << np.arange(bits - 1, -1, -1)
    return (binary.reshape(-1, bits) @ weights).astype(np.uint8)


class _Reader:
    def __init__(self, raw: bytes):
        self.raw, self.pos = raw, 0

    def take(self, count: int) -> bytes:
        if count < 0 or self.pos + count > len(self.raw):
            raise ValueError("Truncated GIF")
        result = self.raw[self.pos:self.pos + count]
        self.pos += count
        return result

    def byte(self) -> int:
        return self.take(1)[0]

    def table(self, flags: int) -> tuple[str, ...]:
        count = 1 << ((flags & 7) + 1)
        if count > PROFILE.max_colors:
            raise ValueError("The working profile allows at most 64 entries")
        return _palette(tuple("#" + self.take(3).hex().upper() for _ in range(count)))

    def blocks(self) -> tuple[bytes, bytes]:
        start, parts = self.pos, []
        while True:
            length = self.byte()
            if not length:
                return self.raw[start:self.pos], b"".join(parts)
            parts.append(self.take(length))


def inspect(raw: bytes) -> list[Frame]:
    reader = _Reader(raw)
    if reader.take(6) not in (b"GIF87a", b"GIF89a"):
        raise ValueError("Expected an indexed GIF")
    width, height, flags, _, _ = struct.unpack("<HHBBB", reader.take(7))
    if (width, height) != (PROFILE.pixel_side, PROFILE.pixel_side):
        raise ValueError("Expected a 256 by 256 pixel canvas")
    global_palette = reader.table(flags) if flags & 0x80 else None
    frames, delay, transparent = [], 0, False
    while True:
        marker = reader.byte()
        if marker == 0x3B:
            if reader.pos != len(raw) or not frames:
                raise ValueError("Invalid GIF termination")
            return frames
        if marker == 0x21:
            label = reader.byte()
            _, data = reader.blocks()
            if label == 0xF9:
                if len(data) != 4:
                    raise ValueError("Invalid graphic control extension")
                delay = int.from_bytes(data[1:3], "little")
                transparent = bool(data[0] & 1)
                if (data[0] >> 2) & 7 not in (0, 1):
                    raise ValueError("Only complete independent frames are supported")
            elif label not in (0xFE, 0xFF):
                raise ValueError("Unsupported graphic extension")
            continue
        if marker != 0x2C:
            raise ValueError("Unexpected GIF block")
        left, top, width, height, flags = struct.unpack("<HHHHB", reader.take(9))
        if (left, top, width, height) != (0, 0, 256, 256) or transparent:
            raise ValueError("Expected a complete opaque frame")
        colors = reader.table(flags) if flags & 0x80 else global_palette
        if colors is None:
            raise ValueError("Missing hexadecimal palette")
        code_size = reader.take(1)
        if not 2 <= code_size[0] <= 8:
            raise ValueError("Invalid LZW code size")
        encoded, _ = reader.blocks()
        frames.append(Frame(colors, delay, code_size + encoded, bool(flags & 0x40)))
        if len(frames) > PROFILE.max_frames:
            raise ValueError("The working profile allows at most 64 frames")
        delay, transparent = 0, False


def single_frame_gif(frame: Frame) -> bytes:
    """Expose a stored state as an independent indexed GIF."""
    colors = _palette(frame.palette_hex)
    flags = 0x80 | 0x70 | (len(colors).bit_length() - 2)
    screen = struct.pack("<HHBBB", 256, 256, flags, 0, 0)
    descriptor = b"\x2C" + struct.pack("<HHHHB", 0, 0, 256, 256,
                                    0x40 if frame.interlaced else 0)
    return b"GIF87a" + screen + _table_bytes(colors) + descriptor + frame.image_data + b"\x3B"


def _frame_dimensions(frame: Frame) -> np.ndarray:
    with Image.open(io.BytesIO(single_frame_gif(frame))) as image:
        if image.mode != "P":
            raise ValueError("The state must decode as indexed data")
        pixels = np.frombuffer(image.tobytes(), np.uint8).reshape(256, 256)
    grid = pixels[::4, ::4]
    if not np.array_equal(pixels, grid.repeat(4, axis=0).repeat(4, axis=1)):
        raise ValueError("A 4 by 4 module contains inconsistent indices")
    if np.any(grid >= len(frame.palette_hex)):
        raise ValueError("Dimension exceeds its hexadecimal palette")
    return grid


def encode(payload_hex: str, *, frames: int | None = None,
           palettes: Sequence[Sequence[str]] | None = None,
           frame_period_ms: int = 125) -> Encoding:
    """Encode hexadecimal octets; timing is quantized cumulatively to 10 ms."""
    payload = _payload(payload_hex)
    if not isinstance(frame_period_ms, int) or not 10 <= frame_period_ms <= 655350:
        raise ValueError("Choose an integer frame period from 10 to 655350 ms")
    first = _palette(palettes[0]) if palettes else DEFAULT_PALETTE
    bits = len(first).bit_length() - 1
    per_frame = PROFILE.effective_side ** 2
    required = max(1, math.ceil(len(payload) * 8 / (per_frame * bits)))
    frames = required if frames is None else frames
    if type(frames) is not int or not required <= frames <= PROFILE.max_frames:
        raise ValueError("Frame count must fit the payload and remain within 64")
    tables = [_palette(p) for p in palettes] if palettes else [first] * frames
    if len(tables) != frames or any(len(p) != len(first) for p in tables):
        raise ValueError("Supply one equally sized hexadecimal palette per frame")
    grids = unpack_dimensions(payload_hex, bits, frames * per_frame).reshape(frames, 64, 64)
    flags = 0x80 | 0x70 | (len(first).bit_length() - 2)
    output = bytearray(b"GIF89a" + struct.pack("<HHBBB", 256, 256, flags, 0, 0))
    output.extend(_table_bytes(first))
    output.extend(b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00")
    total_cs = 0
    for i, grid in enumerate(grids):
        image = Image.frombytes("P", (256, 256), grid.repeat(4, 0).repeat(4, 1).tobytes())
        image.putpalette(_table_bytes(tables[i]))
        buffer = io.BytesIO()
        image.save(buffer, format="GIF", optimize=False, interlace=False)
        stored = inspect(buffer.getvalue())[0]
        delay = (i + 1) * frame_period_ms // 10 - i * frame_period_ms // 10
        total_cs += delay
        output.extend(b"\x21\xF9\x04\x04" + struct.pack("<H", delay) + b"\x00\x00")
        local = 0 if i == 0 else 0x80 | (len(first).bit_length() - 2)
        output.extend(b"\x2C" + struct.pack("<HHHHB", 0, 0, 256, 256, local))
        if i:
            output.extend(_table_bytes(tables[i]))
        output.extend(stored.image_data)
    output.append(0x3B)
    return Encoding(bytes(output), len(payload), frames, len(first), total_cs * 10)


def decode(raw: bytes, *, payload_bytes: int | None = None) -> str:
    frames = inspect(raw)
    bits = len(frames[0].palette_hex).bit_length() - 1
    if any(len(f.palette_hex) != 1 << bits for f in frames):
        raise ValueError("All state palettes must have the same size")
    grids = np.stack([_frame_dimensions(f) for f in frames])
    result = pack_dimensions(grids, bits)
    if payload_bytes is None:
        return result
    if type(payload_bytes) is not int or not 0 <= payload_bytes <= len(result) // 2:
        raise ValueError("Invalid original payload length")
    return result[:payload_bytes * 2]


def pack_address(x: int, y: int, t: int, dimension: int) -> str:
    if any(type(v) is not int or not 0 <= v < 64 for v in (x, y, t, dimension)):
        raise ValueError("All four coordinates must be in 0x00 through 0x3F")
    return f"0x{(((t * 64 + y) * 64 + x) * 64 + dimension):06X}"


def unpack_address(address_hex: str) -> tuple[int, int, int, int]:
    if not isinstance(address_hex, str) or not re.fullmatch(r"0x[0-9A-Fa-f]{6}", address_hex):
        raise ValueError("Expected a six-digit hexadecimal catalogue address")
    value = int(address_hex, 16)
    dimension, x, y, t = value & 0x3F, (value >> 6) & 0x3F, (value >> 12) & 0x3F, value >> 18
    return x, y, t, dimension


def scalar_to_hex(value: int) -> str:
    if type(value) is not int or not 0 <= value <= 0x10FFFF or 0xD800 <= value <= 0xDFFF:
        raise ValueError("Expected a Unicode scalar value")
    return f"0x{value:06X}"


def hex_to_scalar(value: str) -> int:
    if not isinstance(value, str) or not re.fullmatch(r"0x[0-9A-Fa-f]{6}", value):
        raise ValueError("Expected a six-digit hexadecimal scalar")
    scalar = int(value, 16)
    scalar_to_hex(scalar)
    return scalar


def scalar_to_dimensions(value: int) -> tuple[str, ...]:
    scalar_to_hex(value)
    return tuple(f"0x{(value >> shift) & 0x3F:02X}" for shift in (18, 12, 6, 0))


def dimensions_to_scalar(values: Sequence[str]) -> int:
    if len(values) != 4 or any(not isinstance(v, str) or not re.fullmatch(r"0x[0-9A-Fa-f]{2}", v) for v in values):
        raise ValueError("Expected four hexadecimal dimension identifiers")
    result = 0
    for value in values:
        part = int(value, 16)
        if part > 0x3F:
            raise ValueError("Dimension is outside 0x00 through 0x3F")
        result = (result << 6) | part
    scalar_to_hex(result)
    return result

