# Quad-Dimensional DataMatrix: seleção de estado mantido no app

[English](../app-state-flow.md) · [Escopo e limitações](scope-and-limitations.md)

O **aplicativo mantém a sequência**. O usuário seleciona um estado e fornece seu código a um serviço ou site. O serviço é o consumidor ou verificador; não precisa exibir a sequência.

| Etapa | App | Usuário ou serviço receptor |
|---|---|---|
| Carregar | Carrega a sequência local e seu mapeamento de estados para códigos | Aguarda um código selecionado |
| Avançar | Seleciona o próximo estado exibido na cadência escolhida | Observa ou solicita um estado |
| Clicar | Interrompe o avanço e congela o estado exibido | Seleciona o estado atual |
| Copiar | Escreve o código hexadecimal associado na área de transferência | Cola ou consome o código |
| Continuar | Retoma a sequência local quando solicitado | Escolhe outro estado posteriormente |

O exemplo de transporte usa oito frames por segundo. O exemplo de interação usa um estado por minuto. São controles separados. Uma sequência de 64 estados leva oito segundos a 8 fps ou 64 minutos a um estado por minuto.

O visualizador local inicia com um estado por minuto. Sua imagem é um GIF indexado independente para o estado selecionado; por isso, pausar não depende de interromper a animação nativa do navegador. No clique, o visualizador cancela o temporizador antes de copiar. Se o acesso direto à área de transferência estiver indisponível, seleciona o texto hexadecimal para cópia manual.

No exemplo sintético, o código copiado é o payload completo de 3 KiB do estado, escrito como 6.144 dígitos hexadecimais. Essa é uma convenção concreta do estudo. O tamanho do código oferecido ao serviço e sua relação com uma chave permanecem questões do RfD.

A analogia com [TOTP, RFC 6238](https://www.rfc-editor.org/rfc/rfc6238.html) diz respeito a um estado evolutivo mantido no app e a um verificador receptor. A interação não exige que a sequência siga a derivação particular do TOTP.

Referência da área de transferência: [W3C Clipboard API](https://www.w3.org/TR/clipboard-apis/).
