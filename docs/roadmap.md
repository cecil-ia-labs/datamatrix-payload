# Roteiro de investigação

| Etapa | Objetivo | Critério verificável | Estado |
|---|---|---|---|
| M0 | Consolidar capacidade, hexadecimal, geometria e segurança | Paper com fórmulas, fontes e distinção entre prova e medição | Concluído localmente |
| M1 | Reproduzir resultados digitais | JSON anterior idêntico e extensão com sementes registradas | Concluído |
| M2 | Acrescentar redundância e autenticação | Apagamentos RS e roundtrip AES-GCM com rejeições negativas | Concluído no escopo documentado |
| M3 | Localizar a grade e marcar confiança | Decodificar rotação/perspectiva e fornecer apagamentos a partir da imagem | Planejado |
| M4 | Medir captura óptica | Protocolo controlado com dispositivos, exposição, distância e repetições | Planejado |
| M5 | Comparar com JAB Code e QR em área equivalente | Bytes aceitos por área/tempo e taxa de falha em canal comum | Planejado |
| M6 | Implementar transporte para chave pública | Biblioteca HPKE estabelecida, identidade da chave e regras de fragmentação/replay | Planejado |

Decisões futuras devem considerar dados recuperados por área e por segundo sob uma taxa de falha definida, em vez de apenas quantidade de cores. Ampliação da paleta, Gray por eixo, interleaving e pilotos locais são hipóteses de engenharia a comparar.
