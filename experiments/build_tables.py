#!/usr/bin/env python3
"""Generate manuscript tables directly from measured JSON and exact budgets."""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper/tables"
OUT.mkdir(parents=True, exist_ok=True)
baseline = json.loads((ROOT / "results/baseline/resultados.json").read_text())
extended = json.loads((ROOT / "results/extended/results.json").read_text())


def table(name, columns, header, rows, caption):
    text = "\\begin{table}[htbp]\n\\centering\\small\n\\begin{tabular}{" + columns + "}\n\\toprule\n"
    text += header + "\\\\\n\\midrule\n"
    text += "\n".join(row + "\\\\" for row in rows)
    text += "\n\\bottomrule\n\\end{tabular}\n\\caption{" + caption + "}\n\\end{table}\n"
    (OUT / name).write_text(text)


rows = []
for q in [2, 8, 16, 32, 64, 128, 129, 256]:
    b = math.log2(q)
    rows.append(f"{q} & {b:.6f} & {128*128*b/8:.2f} & {7680*4320*b/8e6:.6f}")
table("capacity.tex", "rrrr", "$q$ & $\\log_2q$ & $128\\times128$, bytes & 8K, MB",
      rows, "Teto ideal com uma célula por pixel e sem overhead. Para 129 estados, são valores reais de orçamento; bits e bytes inteiros exigem arredondamento e codificação em blocos.")

images = sorted(baseline["source_images"], key=lambda x:x["width"])
row_specs = [
    ("Pixels", lambda r: r["pixels"]),
    ("Cores presentes", lambda r:r["unique_colors"]),
    ("PNG completo, bytes", lambda r:r["file_bytes"]),
    ("Índices de cinco bits, bytes",lambda r:r["packed_indices_bytes"]),
    ("Paleta RGB, bytes",lambda r:r["palette_bytes"]),
    ("zlib dos índices + paleta, bytes",lambda r:r["zlib_packed_plus_palette_bytes"]),
    ("Entropia marginal, bits/pixel",lambda r:f'{r["marginal_entropy_bits_per_pixel"]:.6f}'),
    ("Distância RGB mínima",lambda r:f'{r["minimum_rgb_distance"]:.4f}'),
]
table("source-images.tex", "lrr", "Medida & $64\\times64$ & $128\\times128$",
      [label+" & "+" & ".join(str(fn(r)) for r in images) for label,fn in row_specs],
      "Medidas nos arquivos fornecidos. Cada PNG possui 32 cores; os números descrevem esses arquivos específicos.")

rows = []
for q in [32,128]:
    for s in [1,2,4]:
        vals=[]
        for channel in ["AWGN16","JPEG95_420","blur06"]:
            r=next(r for r in extended["channel_summary"] if r["colors"]==q and r["module_pixels"]==s and r["channel"]==channel)
            vals.append(f'{100*r["mean_SER"]:.3f}')
        rows.append(f'{q} & {s} & '+" & ".join(vals))
table("channel-selected.tex", "rrrrr", "$q$ & $s$ & Ruído RGB & JPEG 4:2:0 & Desfoque",
      rows, "SER média, em porcentagem, de 12 quadros por condição. Ruído: desvio 16; JPEG: Q95; desfoque: desvio 0,6 pixel. Desvios e intervalos completos constam no CSV.")

rows=[]
for r in extended["rs_erasure_trials"]:
    rows.append(f'{r["erasures_per_block"]} & {r["trials"]} & {r["recovered"]} & {r["refused"]}')
table("rs-secure.tex", "rrrr", "Apagamentos & Ensaios & Recuperados & Recusados", rows,
      "RS(31,23) por avaliação em GF(32). As posições dos apagamentos são fornecidas ao interpolador; não há localização de erros desconhecidos.")

source_hashes={r["file"]:r["original_sha256"] for r in images}
(ROOT / "results/source-fixtures.json").write_text(json.dumps({"scope":"Optional private fixtures, not distributed in repository", "sha256":source_hashes},indent=2)+"\n")
print("Generated four tables from measured results and exact arithmetic.")
