# Quad-Dimensional DataMatrix: technical references

[Português](pt/technical-references.md)

| Reference | Role in the discussion |
|---|---|
| [CompuServe GIF89a](https://www.w3.org/Graphics/GIF/spec-gif89a.txt), reproduced by W3C | Indexed colour tables, complete image blocks, LZW, animation delays, and embedded-protocol context |
| [Pillow: image file formats](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif) | Indexed GIF encoding and decoding used by the research adapter |
| [Unicode 18.0, Chapter 3, §3.9](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-3/) | Scalar domain, encoding forms, and surrogate exclusions |
| [RFC 3629: UTF-8](https://www.rfc-editor.org/rfc/rfc3629.html) | One- to four-octet encoding and well-formed scalar representation |
| [RFC 6238: TOTP](https://www.rfc-editor.org/rfc/rfc6238.html) | Reference for app-held evolving state, temporal derivation, and receiving verification |
| [RFC 5116: AEAD](https://www.rfc-editor.org/rfc/rfc5116.html) | Reference for a later authenticated transport or state binding |
| [W3C Clipboard API](https://www.w3.org/TR/clipboard-apis/) | User-triggered copying of the selected hexadecimal code |

The elementary catalogue and payload counts are derived explicitly in the [model](model.md) and both papers. The project name, working profile, app flow, and candidate Unicode mappings are discussion proposals by **João Paulo De Luca Jr and Jorge Luiz Espanhol**.

## Archival metadata references

[Zenodo deposit metadata](https://developers.zenodo.org/#deposit-metadata) defines the publication/report fields used in [.zenodo.json](../.zenodo.json). [Zenodo metadata precedence](https://help.zenodo.org/docs/github/describe-software/) explains why that file takes precedence over `CITATION.cff` during GitHub release archiving. The [deposit guide](publication.md) records the project-specific fields and workflow. The Clipboard API reference above is a W3C Working Draft; the report metadata cites its [24 June 2026 edition](https://www.w3.org/TR/2026/WD-clipboard-apis-20260624/).
