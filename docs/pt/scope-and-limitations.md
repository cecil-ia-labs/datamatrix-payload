# Quad-Dimensional DataMatrix: Escopo e limitações

[English](../scope-and-limitations.md)

Esta seção reúne as qualificações do RfD. Assim, o argumento matemático e a proposta do app podem ser lidos sem repeti-las em cada seção.

1. **Status.** Este é um request for discussion, com protótipo de trabalho e exemplos reproduzíveis. Interoperabilidade, enquadramento, gestão de chaves, renovação dos estados e protocolo de verificação no serviço continuam como questões de projeto.
2. **Quatro dimensões.** Os quatro eixos são coordenadas lógicas em um catálogo. Uma matriz densa seleciona um identificador de dimension em cada posição e estado temporal. O tamanho $64^4$ do catálogo e a quantidade de bits do payload selecionado descrevem objetos distintos.
3. **Valores hexadecimais.** Hexadecimal é a única representação pública da paleta e dos códigos. GIF89a define a serialização interna do contêiner. Escrever um valor em hexadecimal não adiciona entropia a ele.
4. **Perfil de trabalho.** O protótipo aceita frames completos e opacos de 256 × 256 pixels, 4 × 4 pixels indexados idênticos por módulo efetivo e paletas de 2 a 64 entradas cujo tamanho é uma potência de dois. Preserva até 64 frames, inclusive estados idênticos. O comprimento original do payload é fornecido pelo chamador. Metadados do contêiner, campos de autenticação e redundância ficam fora do orçamento bruto do payload.
5. **Tempo.** O exemplo de 8 fps é uma cadência nominal de reprodução, quantizada nas unidades de delay do GIF. A cadência do app é independente; o exemplo inicia com um estado por minuto. Esses valores não medem velocidade de transferência de rede nem vazão de geração de modelos.
6. **App e autenticação.** O visualizador usa estados sintéticos públicos e copia a cor de seis caracteres de um módulo selecionado. Uma paleta de 64 entradas oferece no máximo 64 alternativas de cor por estado; a largura de seis caracteres não mede a força de autenticação. Demonstra seleção e comportamento da área de transferência. Confidencialidade, derivação, expiração, limitação de tentativas, vínculo com desafios, renovação do ciclo e tratamento de replay requerem projeto revisto separadamente. TOTP e AEAD são referências para essa discussão.
7. **Unicode.** O domínio escalar possui 1.112.064 valores. Caracteres atribuídos, clusters de grafemas, octetos UTF-8, valores escalares, entradas da paleta e chaves secretas são unidades distintas. Mapeamentos hexadecimais um a um são candidatos para representação ou projeto de dicionários. Cardinalidade da paleta, ordenação, caracteres repetidos e armazenamento do dicionário precisam ser contabilizados em um transporte de texto.
8. **Retenção na área de transferência.** A limpeza de 30 segundos é uma tentativa que exige permissão do navegador e página em foco. Confere o texto atual antes de escrever; a API não oferece uma operação atômica de comparar e limpar. O histórico e as cópias em outros aplicativos ficam fora de seu controle. A retenção é independente da expiração do código e das regras de aceitação do serviço receptor.
9. **Evidência.** O estudo valida recuperação exata no perfil digital declarado. Não apresenta alegações de desempenho para modelos generativos nem captura física. A especificação posterior poderá adotar outro perfil após a discussão.

Referências: [GIF89a](https://www.w3.org/Graphics/GIF/spec-gif89a.txt), [Unicode §3.9](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-3/), [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html), [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238.html), [RFC 5116](https://www.rfc-editor.org/rfc/rfc5116.html).

## Leitura dos artefatos distribuídos

O app atual contém 16 estados públicos, com ciclo padrão de interação de 16 minutos. O perfil de 64 estados é o máximo suportado. As gravações da interface usam paleta e geometria de apresentação próprias; as medidas de recuperação usam o arquivo indexado exato do estudo. As [notas da versão](release-notes.md) e o [guia de depósito](publication.md) preservam essas distinções.
