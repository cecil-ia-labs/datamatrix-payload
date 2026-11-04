# Evidência e alcance das afirmações

| Afirmação | Evidência | Alcance |
|---|---|---|
| $N$ células livres com $q$ estados admitem $q^N$ mensagens | Contagem e prova no manuscrito | Canal ideal, estados distinguíveis |
| RGB e `#RRGGBB` preservam os mesmos 24 bits | Identidade e teste de comportamento | Valores digitais, sem captura óptica |
| As duas imagens indexadas têm 32 cores | Leitura dos arquivos e hashes | Arquivos efetivamente fornecidos |
| O benchmark anterior é reproduzível neste ambiente | JSON antigo e reexecução comparados: iguais | Mesmo ambiente e entradas |
| Há efeito conjunto de alfabeto, módulo e perturbação | 648 quadros sintéticos; CSV por realização | Pipeline e ensemble documentados |
| Pilotos podem corrigir centros sob mistura afim global | Quatro testes do benchmark anterior | Duas imagens, transformação global e geometria conhecida |
| RS(31,23) reconstrói até oito apagamentos localizados | Prova da distância mínima e 900 casos recuperados | Apagamentos fornecidos, sem erros desconhecidos adicionais |
| Nove apagamentos são recusados pelo interpolador | 100 casos recusados | Critério implementado: menos de 23 amostras conhecidas |
| AES-GCM sobrevive ao transporte visual exato | 2.048 bytes recuperados e tag verificada | Canal digital sem perturbação, chave simétrica |
| Alteração de ciphertext/AAD/chave é rejeitada nos testes | Três operações geraram InvalidTag | Verificação de integração, não prova nova da cifra |
| Uma paleta pública fixa não fornece sigilo | Inversão explícita; demonstração de texto escolhido | Substituição fixa independente da posição |
| Qubits possuem representação geométrica 3D | Formalismo e documentação IBM | Visualização; não implementação de canal quântico |

## Estatística

Cada uma das 54 condições sintéticas usa 12 quadros. Os erros entre células podem estar correlacionados. A média e o desvio padrão entre quadros são informados; intervalos t para a média são aproximações. O limite unilateral binomial registrado para falha de quadro pressupõe tentativas independentes da mesma distribuição. Zero falhas em 12 tentativas ainda admite limite superior de aproximadamente 22,09% a 95% de confiança nesse modelo.

## Dados e autoria

Os PNGs originais são fixtures privadas opcionais e não são redistribuídos no repositório. Seus nomes e hashes ficam registrados para reprodução autorizada. A extensão sintética, o código e as estatísticas podem ser reproduzidos sem essas imagens.

As contribuições conceituais e a direção do projeto são atribuídas a Juninho De Luca. O manuscrito declara a assistência de ChatGPT/Codex na redação, implementação e execução. Não houve submissão, revisão por pares nem alegação de novidade global nesta etapa.
