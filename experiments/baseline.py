#!/usr/bin/env python3
"""Experimentos reproduzíveis de codificação visual multicolorida.

Não implementa QR/JAB, detecção geométrica, captura por câmera ou FEC.
PNG, índices e hashes são lidos numericamente, sem gerenciamento de cor.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import shutil
import struct
import zlib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, __version__ as pillow_version
from scipy import __version__ as scipy_version
from scipy.ndimage import gaussian_filter
from scipy.spatial import cKDTree
from scipy.spatial.distance import pdist

SEED = 20261104
HEADER = struct.Struct('>4sBI32s')


def palette_grid(q: int) -> np.ndarray:
    if q == 2:
        return np.array([[0, 0, 0], [255, 255, 255]], dtype=np.uint8)
    levels = {8: (2, 2, 2), 16: (4, 2, 2), 32: (4, 4, 2),
              64: (4, 4, 4), 128: (8, 4, 4), 256: (8, 8, 4)}[q]
    axes = [np.rint(np.linspace(0, 255, n)).astype(np.uint8) for n in levels]
    return np.array(np.meshgrid(*axes, indexing='ij')).reshape(3, -1).T.copy()


def pack_indices(indices: np.ndarray, bits: int) -> bytes:
    values = np.asarray(indices, dtype=np.uint16).ravel()
    assert np.all(values < 2 ** bits)
    unpacked = ((values[:, None] >> np.arange(bits - 1, -1, -1)) & 1).astype(np.uint8)
    return np.packbits(unpacked.ravel(), bitorder='big').tobytes()


def unpack_indices(data: bytes, count: int, bits: int) -> np.ndarray:
    unpacked = np.unpackbits(np.frombuffer(data, dtype=np.uint8), bitorder='big')[:count * bits]
    assert unpacked.size == count * bits
    return (unpacked.reshape(-1, bits) @ (1 << np.arange(bits - 1, -1, -1))).astype(np.uint16)


def bytes_to_symbols(data: bytes, bits: int = 5) -> np.ndarray:
    unpacked = np.unpackbits(np.frombuffer(data, dtype=np.uint8), bitorder='big')
    unpacked = np.pad(unpacked, (0, (-len(unpacked)) % bits))
    return (unpacked.reshape(-1, bits) @ (1 << np.arange(bits - 1, -1, -1))).astype(np.uint16)


def nearest(rgb: np.ndarray, palette: np.ndarray) -> np.ndarray:
    return cKDTree(np.asarray(palette, dtype=float)).query(np.asarray(rgb).reshape(-1, 3))[1]


def jpeg_roundtrip(rgb: np.ndarray, quality: int, subsampling: int) -> np.ndarray:
    buffer = io.BytesIO()
    Image.fromarray(np.asarray(rgb, dtype=np.uint8)).save(
        buffer, format='JPEG', quality=quality, subsampling=subsampling)
    buffer.seek(0)
    return np.asarray(Image.open(buffer).convert('RGB')).copy()


def perturb(rgb: np.ndarray, name: str, seed: int) -> np.ndarray:
    rgb = np.asarray(rgb, dtype=np.uint8)
    if name == 'PNG_exato':
        buffer = io.BytesIO()
        Image.fromarray(rgb).save(buffer, format='PNG')
        buffer.seek(0)
        return np.asarray(Image.open(buffer).convert('RGB')).copy()
    if name.startswith('JPEG_'):
        _, quality, sampling = name.split('_')
        return jpeg_roundtrip(rgb, int(quality), 0 if sampling == '444' else 2)
    if name.startswith('AWGN_'):
        sigma = float(name.split('_')[1])
        rng = np.random.default_rng(seed)
        return np.clip(np.rint(rgb + rng.normal(0, sigma, rgb.shape)), 0, 255).astype(np.uint8)
    if name == 'blur_0.6px':
        return np.clip(np.rint(gaussian_filter(rgb.astype(float), sigma=(0.6, 0.6, 0))), 0, 255).astype(np.uint8)
    if name == 'mistura_RGB':
        matrix = np.array([[0.85, 0.08, 0.02], [0.05, 0.70, 0.05], [0.03, 0.05, 0.95]])
        rng = np.random.default_rng(seed)
        received = rgb.astype(float) @ matrix.T + [18, 24, 8]
        received += rng.normal(0, 3, rgb.shape)
        return np.clip(np.rint(received), 0, 255).astype(np.uint8)
    raise ValueError(name)


def make_frame(symbols: np.ndarray, side: int, module: int, palette: np.ndarray) -> np.ndarray:
    assert symbols.size <= side ** 2
    data = np.zeros(side ** 2, dtype=np.uint16)
    data[:symbols.size] = symbols
    grid = np.full((side + 12, side + 8, 3), 255, dtype=np.uint8)
    grid[4:4 + side, 4:4 + side] = palette[data.reshape(side, side)]
    grid[side + 7, 4:36] = palette  # 32 pilotos, geometria previamente conhecida.
    return np.repeat(np.repeat(grid, module, axis=0), module, axis=1)


def sample_region(rgb: np.ndarray, rows: int, cols: int, row: int, col: int, module: int) -> np.ndarray:
    rgb = np.asarray(rgb)
    region = rgb[row * module:(row + rows) * module, col * module:(col + cols) * module]
    cells = region.reshape(rows, module, cols, module, 3).transpose(0, 2, 1, 3, 4)
    lo, hi = (1, module - 1) if module >= 4 else (0, module)
    return cells[:, :, lo:hi, lo:hi].mean(axis=(2, 3))


def extract_frame(rgb: np.ndarray, side: int, module: int, palette: np.ndarray) -> np.ndarray:
    return nearest(sample_region(rgb, side, side, 4, 4, module), palette)


def decode_packet(symbols: np.ndarray) -> tuple[bool, bytes]:
    raw = pack_indices(symbols, 5)
    if len(raw) < HEADER.size:
        return False, b''
    magic, version, length, digest = HEADER.unpack(raw[:HEADER.size])
    if magic != b'CV32' or version != 1 or length > len(raw) - HEADER.size:
        return False, b''
    payload = raw[HEADER.size:HEADER.size + length]
    return hashlib.sha256(payload).digest() == digest, payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=Path(__file__).parent / 'inputs')
    parser.add_argument('--out', type=Path, default=Path(__file__).parent / 'resultados')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    photos, transport_tests, picture_tests, calibration_tests = [], [], [], []
    preview = []
    transport_palette = palette_grid(32)
    cases = ['PNG_exato', 'JPEG_95_444', 'JPEG_95_420', 'JPEG_75_444',
             'JPEG_75_420', 'AWGN_8', 'AWGN_16', 'blur_0.6px']
    for input_i, source in enumerate(sorted(args.inputs.glob('*.png'))):
        original_bytes = source.read_bytes()
        image = Image.open(source)
        assert image.mode == 'P', 'Os testes de índices esperam PNG indexado.'
        width, height = image.size
        indices = np.asarray(image).copy().ravel()
        palette = np.array(image.getpalette(), dtype=np.uint8).reshape(-1, 3)
        assert len(palette) == 32 and len(np.unique(indices)) == 32
        packed = pack_indices(indices, 5)
        recovered_indices = unpack_indices(packed, indices.size, 5)
        assert np.array_equal(recovered_indices, indices)
        original_rgb = np.asarray(image.convert('RGB')).copy()
        assert np.array_equal(palette[recovered_indices].reshape(height, width, 3), original_rgb)
        counts = np.bincount(indices, minlength=32)
        probabilities = counts / counts.sum()
        entropy = float(-(probabilities * np.log2(probabilities)).sum())
        min_distance = float(pdist(palette.astype(float)).min())
        (args.out / f'{source.stem}.indices5').write_bytes(packed)
        (args.out / f'{source.stem}.paleta.json').write_text(json.dumps(
            {'width': width, 'height': height, 'bits_per_index': 5, 'order': 'row-major; MSB-first',
             'palette_rgb': palette.tolist()}, indent=2) + '\n')
        photos.append({'file': source.name, 'width': width, 'height': height,
                       'pixels': int(indices.size), 'file_bytes': len(original_bytes),
                       'png_index_bit_depth': original_bytes[24], 'palette_entries': len(palette),
                       'unique_colors': int(len(np.unique(original_rgb.reshape(-1, 3), axis=0))),
                       'packed_indices_bytes': len(packed), 'palette_bytes': int(palette.size),
                       'zlib_packed_plus_palette_bytes': len(zlib.compress(packed, 9)) + int(palette.size),
                       'marginal_entropy_bits_per_pixel': entropy,
                       'minimum_rgb_distance': min_distance,
                       'exact_index_and_rgb_roundtrip': True,
                       'original_sha256': hashlib.sha256(original_bytes).hexdigest()})
        for palette_name, test_palette in [('paleta_fotografia', palette), ('paleta_transporte32', transport_palette)]:
            rgb = test_palette[indices].reshape(height, width, 3)
            for case_i, case in enumerate(['PNG_exato', 'JPEG_95_444', 'JPEG_95_420', 'AWGN_4', 'AWGN_8']):
                altered = perturb(rgb, case, SEED + input_i * 100 + case_i)
                detected = nearest(altered, test_palette)
                errors = int(np.count_nonzero(detected != indices))
                picture_tests.append({'file': source.name, 'palette': palette_name, 'case': case,
                                      'symbols': int(indices.size), 'symbol_errors': errors,
                                      'symbol_error_rate': errors / indices.size})

        packet = HEADER.pack(b'CV32', 1, len(original_bytes), hashlib.sha256(original_bytes).digest()) + original_bytes
        symbols = bytes_to_symbols(packet)
        side = width
        for module in [1, 2, 4]:
            frame = make_frame(symbols, side, module, transport_palette)
            if module == 4:
                path = args.out / f'{source.stem}.portadora32.png'
                Image.fromarray(frame).save(path)
                # Reabre a PNG efetivamente salva e recupera o PNG original byte a byte.
                stored_frame = np.asarray(Image.open(path).convert('RGB'))
                decoded = extract_frame(stored_frame, side, module, transport_palette)
                valid, recovered = decode_packet(decoded)
                assert valid and recovered == original_bytes
                (args.out / f'{source.stem}.recuperada.png').write_bytes(recovered)
                preview.append((original_rgb, frame, source.name))
            for case_i, case in enumerate(cases):
                altered = perturb(frame, case, SEED + input_i * 100 + module * 10 + case_i)
                detected = extract_frame(altered, side, module, transport_palette)
                used = detected[:symbols.size]
                errors = int(np.count_nonzero(used != symbols))
                xor = np.bitwise_xor(used, symbols)
                bit_errors = int(np.unpackbits(xor.astype(np.uint8)).sum())
                valid, recovered = decode_packet(detected)
                transport_tests.append({'file': source.name, 'module_pixels': module,
                                        'case': case, 'payload_bytes': len(original_bytes),
                                        'header_bytes': HEADER.size, 'symbols': int(symbols.size),
                                        'symbol_errors': errors, 'symbol_error_rate': errors / symbols.size,
                                        'bit_errors': bit_errors, 'bit_error_rate': bit_errors / (symbols.size * 5),
                                        'sha256_valid_and_bytes_equal': bool(valid and recovered == original_bytes)})
            if module == 4:
                altered = perturb(frame, 'mistura_RGB', SEED + input_i)
                observed_palette = sample_region(altered, 1, 32, side + 7, 4, module).reshape(32, 3)
                for calibration, decoder_palette in [('sem_pilotos', transport_palette), ('com_pilotos', observed_palette)]:
                    detected = extract_frame(altered, side, module, decoder_palette)
                    errors = int(np.count_nonzero(detected[:symbols.size] != symbols))
                    valid, recovered = decode_packet(detected)
                    calibration_tests.append({'file': source.name, 'calibration': calibration,
                                              'module_pixels': module, 'symbols': int(symbols.size),
                                              'symbol_errors': errors, 'symbol_error_rate': errors / symbols.size,
                                              'sha256_valid_and_bytes_equal': bool(valid and recovered == original_bytes)})

    # Alfabeto uniforme e independente das fotografias, para estudar densidade de cores.
    constellation_tests = []
    for q in [8, 16, 32, 64, 128, 256]:
        palette = palette_grid(q)
        rng = np.random.default_rng(SEED + q)
        data = rng.integers(0, q, (128, 128))
        for module in [1, 2, 4]:
            rgb = np.repeat(np.repeat(palette[data], module, axis=0), module, axis=1)
            for case_i, case in enumerate(['JPEG_95_444', 'JPEG_95_420', 'AWGN_16', 'blur_0.6px']):
                altered = perturb(rgb, case, SEED + q * 100 + module * 10 + case_i)
                sampled = sample_region(altered, 128, 128, 0, 0, module)
                detected = nearest(sampled, palette).reshape(data.shape)
                errors = int(np.count_nonzero(detected != data))
                constellation_tests.append({'colors': q, 'module_pixels': module, 'case': case,
                                            'symbols': int(data.size), 'symbol_errors': errors,
                                            'symbol_error_rate': errors / data.size,
                                            'minimum_rgb_distance': float(pdist(palette.astype(float)).min())})

    N = 7680 * 4320
    capacities = []
    for q in [2, 8, 16, 32, 64, 128, 129, 256]:
        for module in [1, 2, 4, 8]:
            n = (7680 // module) * (4320 // module)
            raw = n * math.log2(q) / 8
            capacities.append({'colors': q, 'module_pixels': module, 'cells': n,
                               'ideal_bytes': raw, 'ideal_MB': raw / 1e6,
                               'illustrative_bytes_rate_0.8_utilization_0.9': raw * 0.8 * 0.9})
    results = {'date': '2026-11-04', 'seed': SEED,
               'environment': {'numpy': np.__version__, 'Pillow': pillow_version, 'scipy': scipy_version},
               'limitations': ['Simulações digitais; nenhuma captura óptica real.',
                               'Geometria, alinhamento, paleta nominal e dimensão conhecidos.',
                               'Sem FEC; SHA-256 detecta corrupção e não a corrige.',
                               'Distância RGB e ruído artificial não modelam uma câmera completa.',
                               'Resultados de JPEG dependem do encoder, alinhamento e parâmetros.',
                               'Uma realização de ruído por condição; resultados não são estimativas universais.'],
               'source_images': photos, 'picture_palette_tests': picture_tests,
               'transport_tests': transport_tests, 'calibration_tests': calibration_tests,
               'constellation_tests': constellation_tests, 'capacity_calculations': capacities}
    (args.out / 'resultados.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n')
    for name, rows in [('transporte', transport_tests), ('paletas', picture_tests),
                       ('calibracao', calibration_tests), ('constelacoes', constellation_tests),
                       ('capacidades', capacities)]:
        with (args.out / f'{name}.csv').open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
    fig, axes = plt.subplots(2, 2, figsize=(9, 8), facecolor='#f5f7fb')
    for row, (rgb, frame, name) in enumerate(preview):
        axes[row, 0].imshow(rgb, interpolation='nearest')
        axes[row, 0].set_title(f'{name}\nConteúdo: fotografia com 32 cores', fontsize=11)
        axes[row, 1].imshow(frame, interpolation='nearest')
        axes[row, 1].set_title('Transporte: arquivo PNG em símbolos de 5 bits\nRecuperação exata validada por SHA-256', fontsize=11)
        for ax in axes[row]:
            ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle('A paleta da imagem e a paleta do canal têm funções diferentes', fontsize=15)
    fig.text(0.5, 0.015, 'Protótipo sem FEC e sem localização automática por câmera. Geometria conhecida.', ha='center', fontsize=10)
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    fig.savefig(args.out / 'conteudo-e-transporte.png', dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8), sharey=True)
    for ax, case, title in zip(axes, ['JPEG_95_444', 'JPEG_95_420'], ['JPEG Q95 · 4:4:4', 'JPEG Q95 · 4:2:0']):
        for module in [1, 2, 4]:
            rows = [r for r in constellation_tests if r['case'] == case and r['module_pixels'] == module]
            ax.plot([r['colors'] for r in rows], [100 * r['symbol_error_rate'] for r in rows], marker='o', label=f'{module}×{module} px por célula')
        ax.set_xscale('log', base=2)
        ax.set_xticks([8, 16, 32, 64, 128, 256], [8, 16, 32, 64, 128, 256])
        ax.set_title(title); ax.set_xlabel('Cores do alfabeto')
        ax.grid(alpha=0.2); ax.legend(fontsize=8)
    axes[0].set_ylabel('Símbolos incorretos (%)')
    fig.suptitle('Simulação digital: cor, tamanho da célula e subamostragem')
    fig.tight_layout()
    fig.savefig(args.out / 'erros-jpeg.png', dpi=160)
    plt.close(fig)
    print(json.dumps({'source_images': photos,
                      'transport_tests_count': len(transport_tests),
                      'transport_tests': [r for r in transport_tests if r['case'] in ['PNG_exato', 'JPEG_95_444', 'JPEG_95_420']],
                      'calibration_tests': calibration_tests,
                      'picture_tests': picture_tests,
                      'out': str(args.out.resolve())}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
