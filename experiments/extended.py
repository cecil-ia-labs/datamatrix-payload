#!/usr/bin/env python3
"""Synthetic repeat trials, explicit erasures, and authenticated visual transport.

No photographs, optical captures, HPKE implementation, or production keys are
included. AES-GCM keys/nonces exist in memory only and are freshly generated.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import numpy as np
import PIL
import scipy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from scipy.spatial.distance import pdist
from scipy.stats import beta, t
from cryptography import __version__ as crypto_version
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from datamatrix_payload.core import palette, rgb_to_int, bytes_to_symbols, symbols_to_bytes, render, sample, detect, channel
from datamatrix_payload import rs32

SEED = 20261104
HEADER = struct.Struct(">4sBI32s")


def csv_write(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def transport_check():
    rng = np.random.default_rng(SEED)
    plaintext = rng.integers(0, 256, 2048, dtype=np.uint8).tobytes()
    aad = b"datamatrix-payload/v0.1;AES256GCM;RS31-23;RGB32"
    cipher = AESGCM(AESGCM.generate_key(bit_length=256))
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, plaintext, aad)
    envelope = nonce + ciphertext
    packet = HEADER.pack(b"DMPS", 1, len(envelope), hashlib.sha256(envelope).digest()) + envelope
    symbols = bytes_to_symbols(packet)
    coded, count = rs32.encode_stream(symbols)
    rgb = render(coded, palette(32), 128, 4)
    observed = detect(sample(rgb, 128, 4), palette(32))[:len(coded)]
    recovered_symbols = rs32.decode_stream(observed, count)
    recovered_packet = symbols_to_bytes(recovered_symbols, length=len(packet))
    magic, version, length, digest = HEADER.unpack(recovered_packet[:HEADER.size])
    received = recovered_packet[HEADER.size:HEADER.size + length]
    assert magic == b"DMPS" and version == 1 and hashlib.sha256(received).digest() == digest
    assert cipher.decrypt(received[:12], received[12:], aad) == plaintext
    rejected = {}
    altered = bytearray(ciphertext)
    altered[7] ^= 1
    for name, ct, associated, decoder in [
        ("tampered_ciphertext", bytes(altered), aad, cipher),
        ("tampered_aad", ciphertext, aad + b"!", cipher),
        ("wrong_key", ciphertext, aad, AESGCM(AESGCM.generate_key(bit_length=256))),
    ]:
        try:
            decoder.decrypt(nonce, ct, associated)
            rejected[name] = False
        except InvalidTag:
            rejected[name] = True
    assert all(rejected.values())
    return {
        "payload_bytes": len(plaintext), "nonce_bytes": len(nonce),
        "tag_bytes": len(ciphertext) - len(plaintext), "header_bytes": HEADER.size,
        "packet_bytes": len(packet), "uncoded_symbols": len(symbols),
        "rs_blocks": len(coded) // 31, "coded_symbols": len(coded),
        "module_pixels": 4, "matrix_side": 128,
        "exact_authenticated_roundtrip": True, **rejected,
        "scope": "Known geometry; no channel distortion; symmetric AES-GCM, not HPKE",
        "key_handling": "Fresh random key and nonce held only in memory; no secret saved",
    }


def erasure_checks(trials):
    rng = np.random.default_rng(SEED + 800)
    rows = []
    for erased_count in range(10):
        successes = refusals = mismatches = 0
        for _ in range(trials):
            message = rng.integers(0, 32, 23, dtype=np.uint8)
            codeword = rs32.encode(message)
            locations = rng.choice(31, erased_count, replace=False)
            received = codeword.copy()
            received[locations] = 0
            try:
                decoded = rs32.decode_erasures(received, locations)
                successes += int(np.array_equal(decoded, message))
                mismatches += int(not np.array_equal(decoded, message))
            except ValueError:
                refusals += 1
        assert mismatches == 0
        assert successes == trials if erased_count <= 8 else refusals == trials
        rows.append({"erasures_per_block": erased_count, "trials": trials,
                     "recovered": successes, "refused": refusals, "mismatches": mismatches})
    return rows


def repeated_channels(repetitions, side):
    rows, summary = [], []
    for q in [8, 16, 32, 64, 128, 256]:
        colors = palette(q)
        for module in [1, 2, 4]:
            for mode_index, mode in enumerate(["AWGN16", "JPEG95_420", "blur06"]):
                selected = []
                for trial in range(repetitions):
                    seed = SEED + q * 10000 + module * 1000 + mode_index * 100 + trial
                    rng = np.random.default_rng(seed)
                    sent = rng.integers(0, q, side * side, dtype=np.uint16)
                    rgb = render(sent, colors, side, module)
                    received = channel(rgb, mode, rng)
                    predicted = detect(sample(received, side, module), colors)
                    errors = int(np.count_nonzero(predicted != sent))
                    bit_errors = int(np.unpackbits(np.bitwise_xor(predicted, sent).astype(np.uint8)).sum())
                    row = {"colors": q, "module_pixels": module, "channel": mode,
                           "trial": trial, "seed": seed, "symbols": side * side,
                           "symbol_errors": errors, "SER": errors / sent.size,
                           "BER": bit_errors / (sent.size * int(math.log2(q))),
                           "frame_failed": int(errors > 0)}
                    rows.append(row)
                    selected.append(row)
                values = np.array([r["SER"] for r in selected])
                failures = sum(r["frame_failed"] for r in selected)
                mean = float(values.mean())
                margin = float(t.ppf(.975, repetitions - 1) * values.std(ddof=1) / math.sqrt(repetitions))
                summary.append({"colors": q, "module_pixels": module, "channel": mode,
                                "trials": repetitions, "symbols_per_trial": side * side,
                                "mean_SER": mean, "SER_sd_across_frames": float(values.std(ddof=1)),
                                "mean_SER_t95_low": max(0., mean - margin),
                                "mean_SER_t95_high": min(1., mean + margin),
                                "failed_frames": failures, "frame_failure_rate": failures / repetitions,
                                "frame_failure_one_sided95_upper": 1. if failures == repetitions else float(beta.ppf(.95, failures + 1, repetitions - failures)),
                                "nominal_bits_per_rendered_pixel": math.log2(q) / module**2,
                                "empirical_uncoded_exact_frame_goodput_bits_per_pixel": (1-failures/repetitions)*math.log2(q)/module**2})
    return rows, summary


def figures(out, figdir, summary):
    figdir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.3), sharey=True)
    for ax, mode in zip(axes, ["AWGN16", "JPEG95_420", "blur06"]):
        for module in [1, 2, 4]:
            selected = [r for r in summary if r["channel"] == mode and r["module_pixels"] == module]
            ax.plot([r["colors"] for r in selected], [100*r["mean_SER"] for r in selected], marker="o", label=f"{module} x {module} px")
        ax.set_xscale("log", base=2)
        ax.set_xticks([8, 16, 32, 64, 128, 256], [8, 16, 32, 64, 128, 256])
        ax.set_title(mode)
        ax.set_xlabel("Colors q")
        ax.grid(alpha=.2)
    axes[0].set_ylabel("Mean symbol error (%)")
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(figdir / "channel-errors.pdf", bbox_inches="tight")
    fig.savefig(figdir / "channel-errors.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    fig = plt.figure(figsize=(9.8, 4))
    ax = fig.add_subplot(121, projection="3d")
    colors = palette(32)
    ax.scatter(colors[:, 0], colors[:, 1], colors[:, 2], c=colors/255, edgecolors="k", s=65)
    ax.set(xlabel="R", ylabel="G", zlabel="B", title="RGB constellation, q=32")
    ax2 = fig.add_subplot(122)
    q = np.array([2, 8, 16, 32, 64, 128, 256])
    for module in [1, 2, 4]:
        ax2.plot(q, np.log2(q) * (7680//module) * (4320//module) / 8e6, marker="o", label=f"s={module}")
    ax2.set_xscale("log", base=2)
    ax2.set_xticks(q, q)
    ax2.set(xlabel="Colors q", ylabel="Raw ideal capacity (MB)", title="8K, no overhead")
    ax2.legend()
    ax2.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(figdir / "constellation-capacity.pdf", bbox_inches="tight")
    fig.savefig(figdir / "constellation-capacity.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=Path("results/extended"))
    p.add_argument("--figures", type=Path, default=Path("paper/figures"))
    p.add_argument("--repetitions", type=int, default=12)
    p.add_argument("--side", type=int, default=64)
    p.add_argument("--erasure-trials", type=int, default=100)
    args = p.parse_args()
    if args.repetitions < 2 or args.side < 1 or args.erasure_trials < 1:
        p.error("Invalid experiment dimensions")
    args.out.mkdir(parents=True, exist_ok=True)
    rows, summary = repeated_channels(args.repetitions, args.side)
    erasures = erasure_checks(args.erasure_trials)
    secure = transport_check()
    rng = np.random.default_rng(SEED)
    secret_permutation = rng.permutation(128)
    known_plaintext = np.arange(128)
    ciphertext = secret_permutation[known_plaintext]
    recovered_inverse = np.argsort(ciphertext)
    chosen_plaintext_recovers_all = bool(np.array_equal(recovered_inverse[ciphertext], known_plaintext))
    assert chosen_plaintext_recovers_all
    data = {"date": "2026-11-04", "seed": SEED,
            "environment": {"python": platform.python_version(), "numpy": np.__version__, "Pillow": PIL.__version__, "scipy": scipy.__version__, "matplotlib": matplotlib.__version__, "cryptography": crypto_version},
            "design": {"colors": [8,16,32,64,128,256], "modules": [1,2,4], "side": args.side,
                       "repetitions": args.repetitions, "channels": ["AWGN16","JPEG95_420","blur06"]},
            "channel_trials": rows, "channel_summary": summary, "rs_erasure_trials": erasures,
            "secure_transport": secure,
            "palette_substitution": {"symbols":128,"known_symbol_color_pairs":128,
                                     "full_inverse_recovered": chosen_plaintext_recovers_all,
                                     "log2_permutation_count": math.lgamma(129)/math.log(2)},
            "limits": ["Digital synthetic channels only; no optical capture", "Geometry and nominal colors known", "RS decoder handles supplied erasures only", "AEAD test does not implement HPKE or sender authentication", "No independence claim for adjacent symbol errors", "Confidence intervals describe this simulation and randomized frame distribution"]}
    (args.out/"results.json").write_text(json.dumps(data, indent=2)+"\n")
    csv_write(args.out/"channel-trials.csv", rows)
    csv_write(args.out/"channel-summary.csv", summary)
    csv_write(args.out/"rs-erasures.csv", erasures)
    (args.out/"secure-transport.json").write_text(json.dumps(secure, indent=2)+"\n")
    palette_json = [{"index":i,"rgb":[int(x) for x in c],"hex":f"#{rgb_to_int(tuple(int(x) for x in c)):06X}"} for i,c in enumerate(palette(32))]
    (args.out/"palette32.json").write_text(json.dumps(palette_json, indent=2)+"\n")
    figures(args.out, args.figures, summary)
    print(json.dumps({"channel_conditions":len(summary),"channel_trials":len(rows),"rs_trials":sum(r["trials"] for r in erasures),"secure_transport":secure},indent=2))


if __name__ == "__main__":
    main()
