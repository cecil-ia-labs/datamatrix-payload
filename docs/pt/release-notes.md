<!--
SPDX-FileCopyrightText: 2026 Cecil-IA Labs
SPDX-License-Identifier: MIT

Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
Organization: Cecil-IA Labs
Project: Quad-Dimensional DataMatrix

AI-assisted development:
OpenAI ChatGPT and Codex were used as development tools.
Human-directed development and integration.
No OpenAI sponsorship, affiliation, or endorsement is implied.

License: See the repository LICENSE file and SPDX identifier above.
-->

# Quad-Dimensional DataMatrix: RfD 0.2.0

[English](../release-notes.md) · [Preparação do depósito](publication.md)

**João Paulo De Luca Jr · Jorge Luiz Espanhol**

Data do relatório: 4 de novembro de 2026. Versão arquivada: [0.2.0](https://doi.org/10.5281/zenodo.23968974).

Esta versão reúne o catálogo de quatro coordenadas, a implementação de pesquisa com GIF indexado, um estudo reproduzível de 16 estados, um app bilíngue de seleção e recepção e relatórios em inglês e português. Trata-se de um Request for Discussion.

| Evidência ou artefato | Resultado |
|---|---|
| Geometria de trabalho | 256 × 256 pixels armazenados; 64 × 64 módulos efetivos; 4 × 4 pixels indexados idênticos por módulo |
| Paleta ativa e sequência máxima | Paletas com 2 a 64 entradas, em potências de dois; até 64 estados |
| Catálogo máximo | 16.777.216 tuplas candidatas |
| Payload bruto máximo | 192 KiB por ciclo de 64 estados; 24 KiB/s nominais a 8 fps |
| Estudo reproduzido | 16 estados; 64 entradas por estado; 48 KiB recuperados byte a byte; ciclo armazenado de 2.000 ms |
| GIF do estudo | 383.644 bytes; SHA-256 `637f84338d88121bd806e26234f941fde2f566c084c0b04468f891a32224cafe` |
| App local | Seleção do primeiro módulo, último ou coordenadas explícitas; pausa/cópia; destaque por 2,5 segundos; comparação no receptor; limpeza condicional após 30 segundos |
| Ciclo padrão do visualizador | 16 estados a um estado por minuto: 16 minutos |
| PoC gravada | GIF recortado e WebM VP9 de 960 × 900; aproximadamente 36,5 segundos; sem áudio |
| Manuscritos | Markdown, LaTeX gerado e PDFs equivalentes em inglês e português, com uma imagem da interface gravada |

O estudo, os cenários de eventos do app e as verificações do repositório e do arquivo distribuído são reproduzíveis pelo Makefile. O pacote de depósito registra hashes dos fontes e fornece checksums SHA-256. O exemplo sintético público demonstra recuperação digital exata e o comportamento de seleção; o projeto de autenticação e interoperabilidade continua em discussão em Escopo e limitações.

O projeto mantém a licença MIT. A assistência de ChatGPT/Codex é reconhecida nos dois manuscritos. Os autores humanos nomeados são os criadores. O pacote de fontes inclui as gravações e seu manifesto de origem; o `PoC.mp4` original fornecido é identificado por checksum, mas não é redistribuído no repositório.
