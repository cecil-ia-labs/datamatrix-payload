# Quad-Dimensional DataMatrix: demonstração do conceito

[English](README.md) · [Projeto](../../README.pt.md)

Gravação do avanço de estados, pausa e cópia e recepção da cor no app de conceito.

| Arquivo | Dimensões | Cadência nominal | Duração | Tamanho |
|---|---|---:|---:|---:|
| [Prévia animada](quad-dimensional-datamatrix-poc.gif) | 960 × 900 | 8 fps | 36,51 s | 3,82 MiB |
| [Vídeo WebM](quad-dimensional-datamatrix-poc.webm) | 960 × 900 | 8 fps | 36,50 s | 0,87 MiB |

O GIF repete continuamente e usa uma paleta de apresentação gerada com 256 entradas. O WebM usa VP9. A gravação original possui um stream de vídeo e nenhum áudio.

## Enquadramento e origem

A entrada é o `PoC.mp4` fornecido: 1920 × 1080 pixels, 36,3083 segundos. O recorte começa em `x=472, y=124`, com largura `960` e altura `900`. Mantém a área do app, incluindo controles e autores, e remove a interface do navegador e o dock do desktop.

Não houve corte temporal nem alteração de velocidade. A conversão amostra a gravação a 8 fps nominais; os timestamps são representados por cada contêiner de saída. As duas saídas completas foram decodificadas com sucesso, e suas imagens inicial, intermediária e final foram inspecionadas.

[manifest.json](manifest.json) registra checksums da entrada e das saídas, geometria, duração, contagem de frames e versões de processamento.

## Reprodução

O recorte espacial usa FFmpeg. As versões GIF e WebM foram produzidas pelo script associado do Cecil-IA Labs FFmpeg, `skills/ffmpeg-conversion/scripts/run.mjs`, com `action=file`, `fps=8` e `width=960`. A requisição GIF também define `maxColors=256` e `loop=0`.

Estes comandos equivalentes da CLI reproduzem o fluxo com FFmpeg 6.1.1 e toolkit 2.0.0:

```bash
ffmpeg -v error -nostdin -n -i PoC.mp4 -map 0:v:0 \
  -vf crop=960:900:472:124 -c:v libx264 -preset fast -qp 0 \
  -fps_mode vfr -map_metadata -1 cropped.mp4

npm exec --yes --package=@cecilialabs/ffmpeg@2.0.0 -- \
  cecilia-ffmpeg convert file cropped.mp4 --to gif --fps 8 --width 960 \
  --max-colors 256 --loop 0 --output quad-dimensional-datamatrix-poc.gif

npm exec --yes --package=@cecilialabs/ffmpeg@2.0.0 -- \
  cecilia-ffmpeg convert file cropped.mp4 --to webm --fps 8 --width 960 \
  --output quad-dimensional-datamatrix-poc.webm
```
