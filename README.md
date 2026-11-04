# datamatrix-payload

Pesquisa de Juninho De Luca, Cecil-IA Labs, sobre payloads binários em matrizes multicoloridas: capacidade, notação hexadecimal, geometria de cores, canal, calibração, redundância e transporte autenticado.

O projeto contém um manuscrito matemático em português, abstract em inglês, referências primárias, código e resultados reproduzíveis. O nome é um identificador do projeto; o protótipo usa uma matriz visual própria, com geometria conhecida.

## Paper

- [PDF](paper/datamatrix-payload-paper-v0.1.pdf)
- [Texto para leitura no GitHub](paper/paper.md)
- [Fonte LaTeX](paper/main.tex)
- [Referências BibTeX](paper/references.bib)
- [Referências técnicas comentadas](docs/technical-references.md)
- [Evidência, hipóteses e limites](docs/evidence.md)

## Resultados desta versão

| Experimento | Evidência |
|---|---|
| Benchmark anterior com dois PNGs de 32 cores | 144 condições digitais reproduzidas com o mesmo JSON |
| Extensão sintética | 648 quadros em 54 condições, com 12 realizações por condição |
| RS(31,23), GF(32), apagamentos conhecidos | 900 blocos com 0–8 apagamentos recuperados; 100 com 9 recusados |
| AES-256-GCM através da matriz sem perturbação | 2.048 bytes recuperados; ciphertext/AAD alterados e chave diferente rejeitados |
| Substituição fixa com 128 cores | Tabela recuperada a partir de 128 pares conhecidos |

Essas medições caracterizam simulações digitais. O decodificador RS implementado interpola apagamentos informados ao programa. Captura óptica, localização automática da grade, correção de erros desconhecidos e HPKE são próximos desenvolvimentos. Os testes de confidencialidade usam AES-GCM simétrico da biblioteca `cryptography`.

## Reprodução

Python 3.11 ou superior. Para reproduzir o ambiente registrado, usar Python 3.12.14 e `requirements.lock.txt`.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.lock.txt
.venv/bin/pip install --no-deps -e .
make PYTHON=.venv/bin/python test
make PYTHON=.venv/bin/python experiments
make PYTHON=.venv/bin/python tables
make PYTHON=.venv/bin/python paper
make markdown
```

A compilação do paper requer LaTeX com `pdflatex`, `bibtex`, Babel português, Latin Modern, AMS e os pacotes indicados no preâmbulo. A versão Markdown requer Pandoc com citeproc.

Para repetir apenas o benchmark com as imagens originais, colocar cópias locais na pasta ignorada `input/`, conferir os SHA-256 em `results/source-fixtures.json` e executar:

```bash
python3 experiments/baseline.py --inputs input --out tmp/baseline-reproduction
```

Os dados pessoais de entrada não fazem parte do repositório. A extensão sintética não depende deles. Sementes, versões e métricas são registradas em `results/extended/`; as chaves e os nonces AES-GCM são novos e ficam apenas em memória. A demonstração criptográfica é experimental e não fornece um protocolo cliente-servidor completo.

## Organização

| Caminho | Conteúdo |
|---|---|
| `src/datamatrix_payload/` | Empacotamento, RGB/hex, renderização, leitura e RS por apagamentos |
| `experiments/` | Benchmark anterior, ensaios sintéticos e geração automática de tabelas |
| `results/` | JSON, CSV, parâmetros e hashes das fixtures opcionais |
| `paper/` | Fonte, bibliografia, tabelas, figuras e versão Markdown |
| `tests/` | Verificações de comportamento e fronteiras de decodificação |
| `docs/` | Referências técnicas, evidência e roteiro de investigação |

Concepção e direção: **Juninho De Luca**. Redação, implementação e execução assistidas por ChatGPT/Codex, OpenAI, conforme declaração no manuscrito. A versão 0.1 é um manuscrito privado de pesquisa. A licença do repositório consta em [LICENSE](LICENSE).
