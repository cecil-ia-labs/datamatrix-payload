# Quad-Dimensional DataMatrix: RfD 0.2.0

[Português](pt/release-notes.md) · [Deposit preparation](publication.md)

**João Paulo De Luca Jr · Jorge Luiz Espanhol**

Report date: 4 November 2026. Proposed first archive version: `0.2.0`.

This release brings together the four-coordinate catalogue, an indexed-GIF research implementation, a reproducible 16-state study, a bilingual selection-and-reception app, and English and Portuguese reports. It is a Request for Discussion.

| Evidence or artifact | Result |
|---|---|
| Working geometry | 256 × 256 stored pixels; 64 × 64 effective modules; 4 × 4 identical indexed pixels per module |
| Active palette and maximum sequence | Power-of-two palettes of 2 to 64 entries; up to 64 states |
| Maximum catalogue | 16,777,216 candidate tuples |
| Maximum gross payload | 192 KiB per 64-state cycle; nominal 24 KiB/s at 8 fps |
| Reproduced case study | 16 states; 64 entries per state; 48 KiB recovered byte for byte; 2,000 ms stored cycle |
| Case-study GIF | 383,644 bytes; SHA-256 `637f84338d88121bd806e26234f941fde2f566c084c0b04468f891a32224cafe` |
| Local app | First, last, or explicit module selection; pause/copy; 2.5-second highlight; receiver equality check; conditional 30-second clipboard cleanup |
| Default viewer cycle | 16 states at one state per minute: 16 minutes |
| Recorded PoC | 960 × 900 cropped GIF and VP9 WebM; approximately 36.5 seconds; no audio |
| Manuscripts | Equivalent English and Portuguese Markdown, generated LaTeX, and PDFs, with a still from the recorded interface |

The study, app event scenarios, and repository/archive checks are reproducible through the Makefile. The deposit package records source hashes and supplies SHA-256 checksums. The public synthetic example establishes exact digital recovery and selection behaviour; authentication and interoperability design remain topics in Scope and Limitations.

The project keeps its MIT license. ChatGPT/Codex assistance is acknowledged in both manuscripts. The named human authors are the creators. The source package includes the recorded media and its provenance manifest; the supplied original `PoC.mp4` is identified by checksum but is not redistributed in the repository.
