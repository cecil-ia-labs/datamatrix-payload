"""Numeric symbol/color mappings. RGB samples are read without color management."""
from __future__ import annotations

import io
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.spatial import cKDTree


def palette(q: int) -> np.ndarray:
    levels = {2: (2, 1, 1), 8: (2, 2, 2), 16: (4, 2, 2),
              32: (4, 4, 2), 64: (4, 4, 4), 128: (8, 4, 4), 256: (8, 8, 4)}
    if q not in levels:
        raise ValueError("Unsupported alphabet size")
    if q == 2:
        return np.array([[0, 0, 0], [255, 255, 255]], dtype=np.uint8)
    axes = [np.rint(np.linspace(0, 255, n)).astype(np.uint8) for n in levels[q]]
    return np.array(np.meshgrid(*axes, indexing="ij")).reshape(3, -1).T.copy()


def rgb_to_int(rgb: tuple[int, int, int]) -> int:
    if len(rgb) != 3 or any(not isinstance(v, int) or not 0 <= v < 256 for v in rgb):
        raise ValueError("Expected three integer channels in [0,255]")
    r, g, b = rgb
    return (r << 16) | (g << 8) | b


def int_to_rgb(value: int) -> tuple[int, int, int]:
    if not isinstance(value, int) or not 0 <= value < 2**24:
        raise ValueError("Expected an unsigned 24-bit integer")
    return ((value >> 16) & 255, (value >> 8) & 255, value & 255)


def bytes_to_symbols(data: bytes, bits: int = 5) -> np.ndarray:
    if not 1 <= bits <= 8:
        raise ValueError("bits must be in [1,8]")
    unpacked = np.unpackbits(np.frombuffer(data, dtype=np.uint8), bitorder="big")
    unpacked = np.pad(unpacked, (0, (-len(unpacked)) % bits))
    return (unpacked.reshape(-1, bits) @ (1 << np.arange(bits - 1, -1, -1))).astype(np.uint8)


def symbols_to_bytes(symbols: np.ndarray, bits: int = 5, length: int | None = None) -> bytes:
    values = np.asarray(symbols)
    if not 1 <= bits <= 8 or not np.issubdtype(values.dtype, np.integer):
        raise ValueError("Expected integer symbols and bits in [1,8]")
    if np.any(values < 0) or np.any(values >= 2**bits):
        raise ValueError("Symbol outside the alphabet")
    unpacked = ((values.astype(np.uint16).ravel()[:, None] >> np.arange(bits - 1, -1, -1)) & 1).astype(np.uint8)
    raw = np.packbits(unpacked.ravel(), bitorder="big").tobytes()
    if length is not None and not 0 <= length <= len(raw):
        raise ValueError("Invalid original byte length")
    return raw if length is None else raw[:length]


def render(symbols: np.ndarray, colors: np.ndarray, side: int, module: int) -> np.ndarray:
    if side < 1 or module < 1 or len(symbols) > side * side:
        raise ValueError("Invalid frame geometry")
    grid = np.zeros(side * side, dtype=np.uint16)
    grid[:len(symbols)] = symbols
    rgb = colors[grid.reshape(side, side)]
    return np.repeat(np.repeat(rgb, module, axis=0), module, axis=1)


def sample(rgb: np.ndarray, side: int, module: int) -> np.ndarray:
    rgb = np.asarray(rgb)
    if rgb.shape != (side * module, side * module, 3):
        raise ValueError("Image does not match known frame geometry")
    cells = rgb.reshape(side, module, side, module, 3).transpose(0, 2, 1, 3, 4)
    lo, hi = (1, module - 1) if module >= 4 else (0, module)
    return cells[:, :, lo:hi, lo:hi].mean(axis=(2, 3))


def detect(observed: np.ndarray, colors: np.ndarray) -> np.ndarray:
    return cKDTree(colors.astype(float)).query(np.asarray(observed).reshape(-1, 3))[1]


def channel(rgb: np.ndarray, mode: str, rng: np.random.Generator) -> np.ndarray:
    if mode == "AWGN16":
        return np.clip(np.rint(rgb.astype(float) + rng.normal(0, 16, rgb.shape)), 0, 255).astype(np.uint8)
    if mode == "JPEG95_420":
        stream = io.BytesIO()
        Image.fromarray(rgb).save(stream, format="JPEG", quality=95, subsampling=2)
        stream.seek(0)
        return np.asarray(Image.open(stream).convert("RGB")).copy()
    if mode == "blur06":
        return np.clip(np.rint(gaussian_filter(rgb.astype(float), (0.6, 0.6, 0))), 0, 255).astype(np.uint8)
    raise ValueError(mode)
