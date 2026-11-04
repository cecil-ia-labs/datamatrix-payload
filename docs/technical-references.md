# Referências técnicas e relações matemáticas

Juninho De Luca · Cecil-IA Labs · 4 de novembro de 2026.

Estas referências consolidam o estudo anterior e acrescentam hexadecimal, representação de qubits e confidencialidade. O [paper](../paper/main.tex) contém as deduções, hipóteses, resultados e bibliografia serializada em [BibTeX](../paper/references.bib).

## Hexadecimal e o significado de cada cor

Uma cor digital RGB de oito bits por canal pode ser escrita como um vetor `(R,G,B)`, um inteiro de 24 bits ou `#RRGGBB`:

$$u=2^{16}R+2^8G+B.$$

Exemplo: `#FF8000 ↔ RGB(255,128,0) ↔ 0xFF8000`. É uma mudança de representação; seis dígitos hexadecimais preservam os 24 bits. Como texto ASCII, os seis dígitos ocupariam seis bytes, ou sete incluindo `#`, antes de compressão.

Uma paleta de 32 entradas escolhe 32 pontos dentre os $2^{24}$ possíveis. O custo da escolha por módulo é $\log_2 32=5$ bits; o custo de descrever uma entrada RGB é 24 bits. São grandezas distintas. A paleta é um **codebook**: `dimension ↔ índice da paleta ↔ valor hexadecimal`.

Fonte primária: [W3C, CSS Color 4, §5.2](https://www.w3.org/TR/2026/CRD-css-color-4-20261103/#hex-notation), notação hexadecimal e interpretação dos canais.

## Capacidade, fonte e canal

$$N=\lfloor W/s\rfloor\lfloor H/s\rfloor,\qquad L_{\max}=\lfloor N\log_2q\rfloor.$$

Para $q=2^b$, índices podem ser empacotados em $b$ bits. Para outros alfabetos, a aproximação do teto exige blocos. O estado branco pode ser dado ou controle; um estado reservado a preenchimento não equivale a payload livre.

| Conceito | Relação | Fonte primária |
|---|---|---|
| Informação e entropia | $H(X)\le\log_2q$; capacidade depende do canal | [Shannon, 1948](https://www.cs.yale.edu/homes/yry/readings/general/shannon1948.pdf) |
| ASCII | Alfabeto de sete bits e controles | [RFC 20, Cerf, 1969](https://www.rfc-editor.org/rfc/rfc20.html) |
| RGB/hex | Empacotamento reversível de três canais | [W3C CSS Color 4](https://www.w3.org/TR/2026/CRD-css-color-4-20261103/) |
| PNG indexado | Profundidades 1, 2, 4 ou 8; paleta separada | [W3C PNG, terceira edição](https://www.w3.org/TR/2025/REC-png-3-20250624/) |
| QR Code | Até 177 × 177 módulos e 2.953 bytes binários | [DENSO WAVE](https://www.qrcode.com/en/about/standards.html) |
| Data Matrix ECC 200 | 144 × 144; até 1.556 valores de oito bits | [GS1, release 24.0, pp. 313–314](https://ref.gs1.org/standards/genspecs/24.0.0/) |
| Código multicolorido padronizado | Antecedente JAB Code | [ISO/IEC 23634:2022, catálogo IEC](https://webstore.iec.ch/en/publication/75648) |
| Paletas cartesianas | Grade 4 × 4 × 2 para 32 cores | [BSI TR-03137 Part 2, anexo F](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03137/BSI-TR-03137_Part2.pdf?__blob=publicationFile&v=1) |
| Constelações | Menor distância sob AWGN isotrópico; fronteiras de decisão | [Forney, MIT OCW, capítulo 5](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/9c669af76ebf74ffe46645541f1ff6b3_chap_5.pdf) |
| Física do sensor | Ruído de contagem e SNR | [EMVA 1288, Release 4.0 Linear](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) |
| Subamostragem JPEG | Resolução de crominância e opções do codec | [libjpeg-turbo, uso](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/main/doc/usage.txt) |

O documento BSI foi verificado por trechos e histórico indexados no domínio oficial; a abertura direta do PDF retornou indisponibilidade nesta etapa. O catálogo ISO/IEC comprova o antecedente e a norma; esta pesquisa não realizou auditoria de conformidade ISO do protótipo.

## Correção de erros

RS por avaliação polinomial permite conectar símbolos de cinco bits a $\operatorname{GF}(32)$. Para RS(31,23), a distância mínima é 9 e o orçamento convencional é $2e+v\le8$.

A implementação deste repositório reconstrói **apagamentos de localização conhecida**, por interpolação. As posições são fornecidas pelo experimento. Localização de erros desconhecidos e marcação automática de apagamentos ainda não estão implementadas.

Fontes: [Reed e Solomon, 1960, DOI](https://doi.org/10.1137/0108018), [cópia do artigo original](https://sites.math.rutgers.edu/~zeilberg/akherim/reed.pdf), [NASA/JPL, módulo 206 Rev. E, §4.4.2](https://deepspace.jpl.nasa.gov/dsndocs/810-005/206/206E.pdf).

## Máscaras, paletas e criptografia

Uma paleta pública fixa $\pi$ permite inverter $C_i=\pi(M_i)$. Logo $H(M\mid C,\pi)=0$. Se a tabela for secreta, a substituição fixa ainda preserva repetições; uma consulta de texto escolhido que cubra o alfabeto recupera a tabela. Esse argumento é uma análise explícita dessa construção, não uma afirmação de que qualquer máscara seja fraca.

Uma máscara binária uniforme, independente, secreta, do mesmo comprimento da mensagem e usada uma única vez pode implementar $C=M\oplus K$, com sigilo perfeito. Distribuição da chave e autenticação continuam necessárias. Para um protocolo de chave pública, o desenho proposto combina um esquema estabelecido, como HPKE, com a matriz como transporte. Paleta e marcadores podem ser públicos.

| Necessidade | Mecanismo | Referência |
|---|---|---|
| Sigilo perfeito sob condições específicas | One-time pad | [Shannon, 1949](https://doi.org/10.1002/j.1538-7305.1949.tb00928.x) |
| Confidencialidade e integridade ligadas à chave | AEAD | [RFC 5116](https://www.rfc-editor.org/rfc/rfc5116.html) |
| Instância de AEAD | AES-GCM e gestão de nonce | [NIST SP 800-38D](https://csrc.nist.gov/pubs/sp/800/38/d/final) |
| Envio ao destinatário por chave pública | KEM + KDF + AEAD | [RFC 9180, HPKE](https://www.rfc-editor.org/rfc/rfc9180.html) |
| Implementação usada nos testes | AESGCM, rejeição de tag inválida | [Documentação pyca/cryptography](https://cryptography.io/en/stable/hazmat/primitives/aead/) |

O experimento criptográfico executado usa AES-GCM simétrico, sem distribuição de chave pública. HPKE é a arquitetura de referência para a evolução cliente-servidor. Um hash público isolado detecta corrupção, mas não autentica origem nem impede alteração intencional acompanhada de recálculo.

## Três dimensões e qubits

Um qubit vive em $\mathbb C^2$. Seu estado puro tem uma representação por ponto na esfera de Bloch em $\mathbb R^3$, com dois parâmetros independentes. Estados mistos ocupam a bola. RGB pode representar uma descrição clássica aproximada dessas coordenadas:

$$c_k=\operatorname{round}\left[\frac{255}{2}(r_k+1)\right].$$

A associação é geométrica. Uma cor legível dentre 128 estados admite sete bits clássicos; a informação clássica comunicável por um qubit sem emaranhamento previamente compartilhado é limitada a um bit. A capacidade da imagem não recebe um fator quântico por usar três componentes.

Fontes: [IBM Quantum, esfera de Bloch](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/bloch-sphere), [Holevo, artigo original de 1973](https://www.mathnet.ru/eng/ppi903) e [codificação superdensa e limite de Holevo](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/superdense-coding).

## GIF e a dimensão temporal

A extensão temporal foi discutida por **Juninho De Luca e Jorge**. A sequência usa índices $D[t,y,x]$ e uma paleta $P_t$ por frame: $RGB[t,y,x]=P_t(D[t,y,x])$. Para $W\times H$ módulos, $F$ frames e $K=2^b$ entradas, o payload bruto é $\lfloor WHF\log_2K/8\rfloor$ bytes. Os custos das paletas, do contêiner e do protocolo são contabilizados separadamente.

O [estudo reproduzível de 16 frames](../experiments/gif-temporal-16/README.md) confirmou 160 KiB com 32 cores e 192 KiB com 64 cores, com recuperação exata. A rotação de paletas e a repetição da animação não fornecem, por si, sigilo nem expiração do arquivo.

| Conceito | Relação | Fonte primária |
|---|---|---|
| GIF indexado e multiframe | Tabelas RGB globais/locais, LZW e delay em centésimos de segundo | [CompuServe GIF89a, W3C](https://www.w3.org/Graphics/GIF/spec-gif89a.txt) |
| Encoder/decoder utilizado | Paletas, duração, transparência e disposição de frames | [Pillow, formatos de arquivo](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) |
| Autenticação temporal | Segredo compartilhado, contador temporal e rejeição de reutilização | [RFC 6238, TOTP](https://www.rfc-editor.org/rfc/rfc6238.html) |
| Autenticação do transporte | AEAD, dados associados e unicidade de nonce por chave | [RFC 5116](https://www.rfc-editor.org/rfc/rfc5116.html) |
