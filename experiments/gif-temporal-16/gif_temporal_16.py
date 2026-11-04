"""GIF temporal: 16 frames, paletas RGB locais e payload binário exato.

Execute: python3 gif_temporal_16.py
Dependências: numpy e Pillow.
A semente fixa serve à reprodução; nenhuma chave criptográfica é gerada.
"""
from __future__ import annotations
import hashlib
import io
import json
import platform
import struct
from pathlib import Path
import numpy as np
import PIL
from PIL import Image

SIDE = 128
FRAME_COUNT = 16
SEED = 20261104
DELAYS_MS = [120, 130] * 8


def inspect_gif(raw):
    """Lê paletas e descritores do contêiner, sem decodificar LZW."""
    assert raw[:6] == b"GIF89a"
    cursor = 13
    global_colors = None
    if raw[10] & 128:
        size = 3 * (1 << ((raw[10] & 7) + 1))
        global_colors = np.frombuffer(raw[cursor:cursor+size], np.uint8).reshape(-1, 3)
        cursor += size
    frames = []
    delay = 0
    transparent = False
    while True:
        marker = raw[cursor]
        cursor += 1
        if marker == 0x3B:
            assert cursor == len(raw)
            return frames
        if marker == 0x21:
            label = raw[cursor]
            cursor += 1
            blocks = []
            while raw[cursor]:
                size = raw[cursor]
                blocks.append(raw[cursor+1:cursor+1+size])
                cursor += size + 1
            cursor += 1
            if label == 0xF9:
                assert len(blocks) == 1 and len(blocks[0]) == 4
                delay = int.from_bytes(blocks[0][1:3], "little") * 10
                transparent = bool(blocks[0][0] & 1)
            continue
        assert marker == 0x2C
        left, top, width, height, flags = struct.unpack_from("<HHHHB", raw, cursor)
        cursor += 9
        colors = global_colors
        local = bool(flags & 128)
        if local:
            size = 3 * (1 << ((flags & 7) + 1))
            colors = np.frombuffer(raw[cursor:cursor+size], np.uint8).reshape(-1, 3)
            cursor += size
        assert colors is not None
        cursor += 1  # LZW minimum code size
        while raw[cursor]:
            cursor += raw[cursor] + 1
        cursor += 1
        frames.append(dict(colors=colors, local=local, delay_ms=delay,
                           transparent=transparent, rectangle=[left, top, width, height]))
        delay = 0
        transparent = False


def to_indices(payload, bits):
    binary = np.unpackbits(np.frombuffer(payload, np.uint8), bitorder="big")
    weights = 1 << np.arange(bits-1, -1, -1)
    return (binary.reshape(-1, bits) @ weights).astype(np.uint8)


def from_indices(indices, bits):
    binary = (indices.reshape(-1, 1).astype(np.uint16) >> np.arange(bits-1, -1, -1)) & 1
    return np.packbits(binary.astype(np.uint8), bitorder="big").tobytes()


def encode(payload, bits, rng):
    grids = to_indices(payload, bits).reshape(FRAME_COUNT, SIDE, SIDE)
    images = []
    for grid in grids:
        # Cada frame escolhe suas K cores dentre todos os valores RGB de 24 bits.
        rgb24 = rng.choice(1 << 24, size=1 << bits, replace=False).astype(np.uint32)
        colors = np.column_stack([(rgb24 >> 16) & 255, (rgb24 >> 8) & 255, rgb24 & 255])
        frame = Image.frombytes("P", (SIDE, SIDE), grid.tobytes())
        frame.putpalette(colors.astype(np.uint8).ravel().tolist())
        images.append(frame)
    stream = io.BytesIO()
    images[0].save(stream, format="GIF", save_all=True, append_images=images[1:],
                   duration=DELAYS_MS, loop=0, disposal=1, optimize=False, interlace=False)
    return stream.getvalue()


def decode(raw, bits):
    # As tabelas usadas para recuperar os índices são lidas do GIF recebido.
    frames = inspect_gif(raw)
    image = Image.open(io.BytesIO(raw))
    assert image.n_frames == len(frames)
    restored = []
    for i, frame in enumerate(frames):
        assert not frame["transparent"]
        assert frame["rectangle"] == [0, 0, SIDE, SIDE]
        colors = frame["colors"].astype(np.uint32)
        assert len(colors) == 1 << bits
        table = (colors[:, 0] << 16) | (colors[:, 1] << 8) | colors[:, 2]
        assert len(np.unique(table)) == len(table)
        order = np.argsort(table)
        image.seek(i)
        rgb = np.asarray(image.convert("RGB"), dtype=np.uint32)
        values = (rgb[..., 0] << 16) | (rgb[..., 1] << 8) | rgb[..., 2]
        loc = np.searchsorted(table[order], values)
        assert np.all(loc < len(table))
        assert np.array_equal(table[order][loc], values)
        restored.append(order[loc].astype(np.uint8))
    return from_indices(np.stack(restored), bits), frames


def main():
    destination = Path(__file__).resolve().parent
    rng = np.random.default_rng(SEED)
    cases = []
    for bits in (5, 6):
        count = SIDE * SIDE * FRAME_COUNT * bits // 8
        payload = rng.integers(0, 256, count, dtype=np.uint8).tobytes()
        raw = encode(payload, bits, rng)
        restored, frames = decode(raw, bits)
        assert restored == payload
        assert len(frames) == FRAME_COUNT
        assert [f["delay_ms"] for f in frames] == DELAYS_MS
        assert sum(f["local"] for f in frames) == FRAME_COUNT - 1
        filename = f"datamatrix-16frames-{1 << bits}cores.gif"
        (destination / filename).write_bytes(raw)
        cases.append(dict(filename=filename, colors=1 << bits, bits_per_module=bits,
                          frames=len(frames), duration_ms=sum(DELAYS_MS),
                          nominal_average_fps=FRAME_COUNT * 1000 / sum(DELAYS_MS),
                          payload_bytes=len(payload), gif_file_bytes=len(raw),
                          payload_sha256=hashlib.sha256(payload).hexdigest(),
                          restored_sha256=hashlib.sha256(restored).hexdigest(),
                          gif_sha256=hashlib.sha256(raw).hexdigest(),
                          exact_recovery=restored == payload,
                          palette_entries_per_frame=1 << bits,
                          local_color_tables=sum(f["local"] for f in frames)))
    result = dict(seed=SEED, python=platform.python_version(), numpy=np.__version__,
                  Pillow=PIL.__version__, modules=[SIDE, SIDE], cases=cases)
    (destination / "resultados-16frames.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

