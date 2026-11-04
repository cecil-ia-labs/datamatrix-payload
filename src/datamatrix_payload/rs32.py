"""Evaluation-form RS(31,23) over GF(32), with ERASURE decoding only.

This research implementation does not locate unknown errors. Erasure positions
are supplied by the experiment. It is not a hardened production FEC library.
"""
from __future__ import annotations
import numpy as np

N, K = 31, 23
PRIMITIVE_POLYNOMIAL = 0b100101  # x^5 + x^2 + 1


def _multiply(a: int, b: int) -> int:
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 32:
            a ^= PRIMITIVE_POLYNOMIAL
    return out


MUL = np.array([[_multiply(a, b) for b in range(32)] for a in range(32)], dtype=np.uint8)
INV = np.zeros(32, dtype=np.uint8)
for _a in range(1, 32):
    INV[_a] = np.flatnonzero(MUL[_a] == 1)[0]
POINTS = []
_x = 1
for _ in range(N):
    POINTS.append(_x)
    _x = _multiply(_x, 2)
assert len(set(POINTS)) == N and _x == 1
GENERATOR = np.ones((N, K), dtype=np.uint8)
for _j in range(1, K):
    GENERATOR[:, _j] = MUL[GENERATOR[:, _j - 1], POINTS]


def _validated(values: np.ndarray, size: int) -> np.ndarray:
    values = np.asarray(values)
    if values.shape != (size,) or not np.issubdtype(values.dtype, np.integer):
        raise ValueError(f"Expected {size} integer symbols")
    if np.any(values < 0) or np.any(values > 31):
        raise ValueError("GF(32) symbols must be in [0,31]")
    return values.astype(np.uint8)


def encode(message: np.ndarray) -> np.ndarray:
    message = _validated(message, K)
    return np.bitwise_xor.reduce(MUL[GENERATOR, message], axis=1)


def decode_erasures(codeword: np.ndarray, erased: np.ndarray | list[int]) -> np.ndarray:
    codeword = _validated(codeword, N)
    erased = np.asarray(erased, dtype=int)
    if erased.ndim != 1 or np.any(erased < 0) or np.any(erased >= N) or len(np.unique(erased)) != len(erased):
        raise ValueError("Invalid erasure locations")
    known = np.setdiff1d(np.arange(N), erased)
    if len(known) < K:
        raise ValueError("More than eight erasures")
    chosen = known[:K]
    matrix = np.column_stack([GENERATOR[chosen].copy(), codeword[chosen]])
    for col in range(K):
        pivots = np.flatnonzero(matrix[col:, col])
        if not len(pivots):
            raise ValueError("Singular interpolation system")
        pivot = col + pivots[0]
        matrix[[col, pivot]] = matrix[[pivot, col]]
        matrix[col] = MUL[matrix[col], INV[matrix[col, col]]]
        for row in range(K):
            if row != col and matrix[row, col]:
                matrix[row] ^= MUL[matrix[col], matrix[row, col]]
    message = matrix[:, -1]
    if np.any(encode(message)[known] != codeword[known]):
        raise ValueError("Non-erased symbols are inconsistent; unknown errors may be present")
    return message


def encode_stream(symbols: np.ndarray) -> tuple[np.ndarray, int]:
    values = np.asarray(symbols).ravel()
    if not len(values) or not np.issubdtype(values.dtype, np.integer) or np.any(values < 0) or np.any(values > 31):
        raise ValueError("Expected non-empty GF(32) integer stream")
    values = values.astype(np.uint8)
    blocks = np.pad(values, (0, (-len(values)) % K)).reshape(-1, K)
    return np.concatenate([encode(block) for block in blocks]), len(values)


def decode_stream(codewords: np.ndarray, original_count: int) -> np.ndarray:
    values = np.asarray(codewords)
    if values.ndim != 1 or not np.issubdtype(values.dtype, np.integer) or np.any(values < 0) or np.any(values > 31):
        raise ValueError("Expected GF(32) integer codewords")
    if len(values) % N or not 0 < original_count <= len(values) // N * K:
        raise ValueError("Invalid stream lengths")
    return np.concatenate([decode_erasures(block, []) for block in values.reshape(-1, N)])[:original_count]
