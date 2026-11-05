# Quad-Dimensional DataMatrix: referências técnicas

[English](../technical-references.md)

| Referência | Papel na discussão |
|---|---|
| [CompuServe GIF89a](https://www.w3.org/Graphics/GIF/spec-gif89a.txt), reproduzido pelo W3C | Tabelas de cor indexadas, blocos completos de imagem, LZW, delays e contexto de protocolo embutido |
| [Pillow: formatos de arquivo](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif) | Codificação e decodificação do GIF indexado usadas pelo adaptador de pesquisa |
| [Unicode 18.0, Capítulo 3, §3.9](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-3/) | Domínio escalar, formas de codificação e exclusão de surrogates |
| [RFC 3629: UTF-8](https://www.rfc-editor.org/rfc/rfc3629.html) | Codificação de um a quatro octetos e representação bem formada de escalares |
| [RFC 6238: TOTP](https://www.rfc-editor.org/rfc/rfc6238.html) | Referência para estado evolutivo mantido no app, derivação temporal e verificação receptora |
| [RFC 5116: AEAD](https://www.rfc-editor.org/rfc/rfc5116.html) | Referência para um transporte autenticado ou vínculo de estado posterior |
| [W3C Clipboard API](https://www.w3.org/TR/clipboard-apis/) | Cópia do código hexadecimal selecionado por ação do usuário |

As contagens elementares de catálogo e payload são deduzidas no [modelo](model.md) e nos dois papers. O nome do projeto, o perfil de trabalho, o fluxo do app e os mapeamentos Unicode candidatos são propostas de discussão de **João Paulo De Luca Jr e Jorge Luiz Espanhol**.

## Referências dos metadados de arquivamento

Os [metadados de depósito do Zenodo](https://developers.zenodo.org/#deposit-metadata) definem os campos de publicação/relatório usados em [.zenodo.json](../../.zenodo.json). A [precedência dos metadados](https://help.zenodo.org/docs/github/describe-software/) explica por que esse arquivo prevalece sobre `CITATION.cff` no arquivamento de releases do GitHub. O [guia de depósito](publication.md) registra os campos e o fluxo específicos do projeto. A referência da Clipboard API acima é um Working Draft do W3C; os metadados citam sua [edição de 24 de junho de 2026](https://www.w3.org/TR/2026/WD-clipboard-apis-20260624/).
