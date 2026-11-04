# Quad-Dimensional DataMatrix: concept demonstration

[Português](README.pt.md) · [Project](../../README.md)

Recorded walkthrough of state advancement, pause and copy, and color reception in the concept app.

| Asset | Dimensions | Nominal cadence | Duration | Size |
|---|---|---:|---:|---:|
| [Animated preview](quad-dimensional-datamatrix-poc.gif) | 960 × 900 | 8 fps | 36.51 s | 3.82 MiB |
| [WebM video](quad-dimensional-datamatrix-poc.webm) | 960 × 900 | 8 fps | 36.50 s | 0.87 MiB |

The GIF loops continuously and uses a generated 256-entry presentation palette. WebM uses VP9. The source recording has one video stream and no audio.

## Framing and provenance

The input is the supplied `PoC.mp4`: 1920 × 1080 pixels, 36.3083 seconds. The crop starts at `x=472, y=124`, with width `960` and height `900`. It retains the app area, including the controls and authors, and removes browser chrome and the desktop dock.

No temporal trim or speed change was applied. Conversion samples the recording at a nominal 8 fps; timestamps are represented by each output container. Both complete outputs were decoded successfully and their first, middle, and final images were inspected.

[manifest.json](manifest.json) records input and output checksums, geometry, duration, frame counts, and processing versions.

## Reproduce

The spatial crop uses FFmpeg. The GIF and WebM renditions were produced through the Cecil-IA Labs FFmpeg associated script `skills/ffmpeg-conversion/scripts/run.mjs`, with `action=file`, `fps=8`, and `width=960`. The GIF request additionally sets `maxColors=256` and `loop=0`.

These equivalent CLI commands reproduce the workflow with FFmpeg 6.1.1 and toolkit 2.0.0:

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
