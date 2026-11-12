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

# Quad-Dimensional DataMatrix: seleção de estado mantido no app

[English](../app-state-flow.md) · [Escopo e limitações](scope-and-limitations.md)

O **aplicativo mantém a sequência**. O usuário seleciona um estado e fornece seu código a um serviço ou site. O serviço é o consumidor ou verificador; não precisa exibir a sequência.

| Etapa | App | Usuário ou serviço receptor |
|---|---|---|
| Carregar | Carrega a sequência local e seu mapeamento de estados para códigos | Aguarda um código selecionado |
| Avançar | Exibe o próximo estado na cadência escolhida | Observa ou solicita um estado |
| Clicar | Congela o estado exibido e seleciona seu módulo | Seleciona o estado atual |
| Copiar | Copia seis caracteres hexadecimais maiúsculos, sem `#` inicial | Recebe um valor como `F519DA` |
| Destacar | Contorna a matriz com a cor escolhida durante 2,5 segundos | Identifica visualmente a cor selecionada |
| Colar | Lê a área de transferência após clique ou toque no círculo receptor | Preenche o círculo com a cor correspondente e mostra sucesso |
| Continuar | Retoma a sequência local quando solicitado | Escolhe outro estado posteriormente |

O exemplo de transporte usa oito frames por segundo. O exemplo de interação inicia com um estado por minuto. Uma sequência de 64 estados leva oito segundos a 8 fps ou 64 minutos a um estado por minuto.

O visualizador distribuído carrega **16 estados sintéticos**. Seu ciclo real dura dois segundos a 8 fps ou 16 minutos na cadência padrão. O ciclo de 64 estados descreve o perfil máximo suportado. A [PoC gravada](../media/README.pt.md) mostra a interface, enquanto o [GIF do estudo](../../examples/quad-dimensional-datamatrix-16-states.gif) é o contêiner que transporta dados.

## Escolha do código

O visualizador copia a entrada hexadecimal da paleta correspondente ao módulo selecionado. O estado completo continua disponível ao decoder de transporte; copiar uma cor não copia esse payload.

| Regra de seleção | Coordenadas | Status |
|---|---|---|
| Primeiro módulo | `(0, 0)` | Padrão no visualizador |
| Último módulo | `(63, 63)` | Disponível em Origem do código |
| Coordenadas explícitas | `(x, y)` escolhidas pelo usuário, ambas de 0 a 63 | Disponível em Origem do código |
| Coordenadas declaradas no início da matriz | Por exemplo, os dois primeiros índices de dimension codificam `x` e `y` | Candidato do RfD; não implementado |

As coordenadas se referem à grade efetiva de 64 × 64 módulos, com origem no canto superior esquerdo. O gerador registra os índices dos módulos e a paleta como valores hexadecimais; assim, o visualizador lê a mesma cor do GIF indexado.

O visualizador renderiza cada estado como um GIF independente. O clique interrompe o temporizador do app antes de copiar. O console extenso do payload foi removido. Se a cópia direta estiver indisponível, um campo pequeno revela apenas o código de seis caracteres para cópia manual. Se a leitura da área de transferência for bloqueada, é oferecido um campo de colagem nativa/digitação. O círculo receptor aceita `#` inicial opcional e letras maiúsculas ou minúsculas, normaliza o texto e informa sucesso apenas quando ele corresponde à última seleção.

## Retenção na área de transferência

Uma cópia bem-sucedida agenda a limpeza para 30 segundos depois. Uma nova cópia reinicia esse intervalo. A limpeza confere o texto atual da área de transferência e tenta apagá-lo apenas quando ainda corresponde ao código escrito pelo app.

A limpeza automática exige página visível e em foco, com permissão de leitura já concedida. O temporizador não abre uma solicitação de permissão. Se a página estiver em segundo plano, tenta novamente no retorno. Quando o navegador bloqueia a limpeza, é oferecida uma ação para limpar; ela também confere o conteúdo atual antes de escrever.

Essa retenção é uma tentativa de limpeza, sem definir expiração do código ou regra de aceitação do serviço receptor. O navegador não fornece uma operação atômica de comparar e limpar; histórico da área de transferência e cópias em outros aplicativos ficam fora do controle da página. Essas fronteiras são reunidas em [Escopo e limitações](scope-and-limitations.md).

A analogia com [TOTP, RFC 6238](https://www.rfc-editor.org/rfc/rfc6238.html) diz respeito a um estado evolutivo mantido no app e a um verificador receptor. Não exige que a sequência siga a derivação do TOTP.

Referência da área de transferência: [W3C Clipboard API](https://www.w3.org/TR/clipboard-apis/).
