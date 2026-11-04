# Estudo de caso: DataMatrix temporal em GIF, 16 frames

Proposta de extensão temporal discutida por **Juninho De Luca e Jorge** em 4 de novembro de 2026. Este estudo trata o GIF como contêiner de dados digitais indexados.

## Escopo e reprodução

- Matriz: 128 × 128 módulos; um pixel por módulo.
- Sequência: 16 frames distintos; 2 segundos nominais por ciclo, a 8 fps em média.
- Casos: 32 e 64 cores, com uma tabela RGB diferente por frame.
- Dados: bytes pseudoaleatórios reproduzíveis, semente 20261104. Não há segredo criptográfico neste experimento.
- Comando: `python3 gif_temporal_16.py`.
- Ambiente registrado: Python 3.12.14, NumPy 2.3.5, Pillow 13.0.0.

O GIF usa uma tabela global para o primeiro frame e 15 tabelas locais para os demais. Cada entrada contém três canais RGB de 8 bits. Todas as cores usadas são distintas dentro de cada tabela. O decoder lê as tabelas diretamente do arquivo recebido e inverte o mapeamento RGB → índice, sem depender das tabelas mantidas pelo encoder.

A semântica é:

`dimension ↔ índice da paleta ↔ valor hexadecimal RGB`

O significado do índice pode permanecer fixo enquanto sua cor muda entre frames. As tabelas estão no arquivo e são públicas.

## Capacidade e resultados

Para K estados por módulo, W × H módulos e F frames:

$$B_{bruto}=\left\lfloor\frac{WHF\log_2 K}{8}\right\rfloor.$$

| Cores | Bits/módulo | Payload por frame | Payload nos 16 frames | Tamanho do GIF |
|---|---:|---:|---:|---:|
| 32 | 5 | 10.240 bytes | 163.840 bytes = 160 KiB | 213.329 bytes |
| 64 | 6 | 12.288 bytes | 196.608 bytes = 192 KiB | 278.783 bytes |

Os dois payloads foram recuperados byte a byte, com SHA-256 idêntico ao original. Foram verificados a quantidade de frames, a duração nominal total, as tabelas locais, a ausência de transparência e os retângulos completos de 128 × 128 pixels.

Os valores da tabela usam toda a matriz para payload. Um protocolo completo precisará reservar espaço para versão, sessão, sequência, comprimento e autenticação. O tamanho do arquivo inclui as tabelas, LZW e os demais campos do GIF. Os dados pseudoaleatórios ampliaram o tamanho do arquivo; a compressão LZW não garante redução.

O delay do GIF é medido em centésimos de segundo. Foram alternados delays de 120 e 130 ms para somar 2.000 ms em 16 frames. A medida descreve o arquivo, sem aferir pontualidade de reprodução em um aplicativo. O loop repete os mesmos dados.

## Matriz temporal e segurança

Podemos representar os índices por $D[t,y,x]\in\{0,\ldots,K-1\}$ e as cores por uma função $P_t$, obtendo $RGB[t,y,x]=P_t(D[t,y,x])$.

O número de matrizes possíveis é $K^{WHF}$; a informação correspondente é $WHF\log_2K$ bits. Assim, o número de possibilidades é exponencial e a capacidade em bytes cresce linearmente com os frames.

A mudança de paleta pode fazer parte do protocolo. A confidencialidade depende de criptografia autenticada e de segredos adequados. Uma tabela incluída no GIF não constitui uma chave secreta.

A analogia com TOTP é útil para expiração e verificação de frescor. No TOTP, um segredo compartilhado alimenta uma função com contador temporal. A animação de um GIF não faz o arquivo expirar: todos os frames já estão disponíveis a quem o possui. A aplicação receptora precisa verificar validade e impedir reutilização de sessões aceitas.

Para uma evolução autenticada, cada frame pode carregar sessão, índice, total de frames e comprimento; esses campos devem estar ligados ao payload pela autenticação. AES-GCM exige unicidade de nonce por chave. A escolha de um desenho criptográfico e sua validação ficam para uma etapa própria.

O uso de T2I/I2I para produzir conteúdo pode anteceder o encoder. A cadência de reprodução de 8 fps não comprova que um modelo gere ou preserve uma sequência arbitrária de índices exatos. O presente teste usa um encoder determinístico.

## Referências primárias

- [GIF89a, especificação CompuServe reproduzida no W3C](https://www.w3.org/Graphics/GIF/spec-gif89a.txt): tabelas de cor, blocos de imagem, delay e LZW.
- [Pillow, formatos de arquivo](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html): GIF multiframe e opções do encoder.
- [RFC 6238, TOTP](https://www.rfc-editor.org/rfc/rfc6238.html): segredo compartilhado, contador temporal e uso único.
- [RFC 5116, AEAD](https://www.rfc-editor.org/rfc/rfc5116.html): autenticação, dados associados e nonces.

