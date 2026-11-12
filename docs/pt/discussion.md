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

# Quad-Dimensional DataMatrix: agenda de discussão

[English](../discussion.md) · [Escopo e limitações](scope-and-limitations.md)

O RfD convida à discussão das escolhas abaixo. O protótipo fornece exemplos, em vez de respostas normativas.

| Tema | Questões |
|---|---|
| Catálogo de quatro coordenadas | Quais aplicações precisam de um endereço do catálogo, um estado denso ou um evento esparso? |
| Dicionário hexadecimal | Uma dimension deve nomear uma entrada da paleta, um escalar Unicode, uma entrada externa da chave ou um código derivado? |
| Unicode | O texto deve usar octetos UTF-8, mapeamento escalar de quatro dimensions ou dicionário adaptativo com até 64 entradas ativas por estado? |
| Posse da sequência | Como a sequência mantida no app é provisionada, renovada e associada ao serviço receptor? |
| Seleção | O clique deve congelar até a retomada explícita, até o consumo ou até um novo desafio? |
| Cadência | Quais casos precisam de 8 fps, um estado por minuto ou avanço comandado pelo usuário? |
| Área de transferência | O visualizador usa uma cor selecionada de seis caracteres. A seleção deve usar o primeiro módulo, o último, coordenadas explícitas ou coordenadas declaradas no cabeçalho da matriz? |
| Autenticação | Como associar o estado selecionado a uma sessão, desafio ou janela de aceitação? |
| Enquadramento | Onde ficam comprimento do payload, versão, identidade do estado e dados de integridade? |
| Evidência | Quais experimentos posteriores permitiriam decidir entre os mapeamentos candidatos? |

A proposta Unicode é particularmente concreta: cada escalar possui um inteiro hexadecimal único. Esse inteiro cabe no catálogo de quatro coordenadas de 24 bits ou em quatro identificadores de dimension de seis bits. O RfD pergunta qual interpretação é útil como entrada na eventual chave ou dicionário.

As [notas da versão 0.2.0](release-notes.md) delimitam o estudo implementado e o comportamento do app. O [guia de depósito](publication.md) prepara este RfD como relatório técnico com material de apoio reproduzível; as questões de discussão continuam abertas.
