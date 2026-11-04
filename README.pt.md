# Quad-Dimensional DataMatrix

**Request for Discussion (RfD), versão 0.2.0.**

**João Paulo De Luca Jr · Jorge Luiz Espanhol**

Cecil-IA Labs · 4 de novembro de 2026

[English](README.md) · [Paper em inglês](paper/quad-dimensional-datamatrix.en.pdf) · [Paper em português](paper/quad-dimensional-datamatrix.pt.pdf)

Quad-Dimensional DataMatrix explora um catálogo com quatro coordenadas lógicas: posição horizontal, posição vertical, estado temporal e dimension hexadecimal. Um GIF indexado transporta a sequência correspondente. Inglês é o idioma padrão; português é a alternativa.

## Perfil de trabalho

| Propriedade | Perfil atual de discussão |
|---|---|
| Contêiner | GIF indexado |
| Frame armazenado | 256 × 256 pixels |
| Matriz efetiva | 64 × 64 módulos |
| Módulo | 4 × 4 pixels indexados idênticos |
| Paleta | Até 64 entradas hexadecimais distintas |
| Sequência | Até 64 frames |
| Exemplo de transporte | 8 frames por segundo |
| Exemplo de interação no app | Um estado por minuto; clique para pausar e copiar |

O mapeamento público é:

**dimension ↔ índice da paleta ↔ valor hexadecimal**

O protótipo usa frames completos e paletas cujo tamanho é uma potência de dois. Seus valores de cor são escritos exclusivamente como entradas hexadecimais de seis dígitos, por exemplo `#12ABEF`.

## Catálogo e payload

Para o perfil máximo:

$$|\Omega|=64\cdot64\cdot64\cdot64=16.777.216.$$

Essa contagem representa tuplas candidatas de quatro coordenadas. Em um ciclo nominal de oito segundos, são **2.097.152 tuplas candidatas por segundo**. Há 262.144 módulos selecionados por ciclo; cada um escolhe uma entre 64 entradas e transporta seis bits.

| Grandeza | Perfil máximo a 8 fps |
|---|---:|
| Entradas candidatas do catálogo | 16.777.216 |
| Módulos selecionados por ciclo | 262.144 |
| Payload bruto por frame | 3 KiB |
| Payload bruto por ciclo de 64 frames | 192 KiB |
| Taxa bruta nominal | 24 KiB/s |

O [modelo matemático](docs/pt/model.md) apresenta a dedução e a seção [Escopo e limitações](docs/pt/scope-and-limitations.md) reúne a interpretação.

## Seleção de estado no app

A sequência fica no **app**. Um usuário, serviço ou site consome um estado selecionado. O app pode avançar um estado por minuto, independentemente do exemplo de transporte. Ao clicar na matriz, o estado exibido é pausado e seu código hexadecimal é copiado.

O [visualizador local](examples/index.html) implementa essa interação em inglês e português. Inicia com um estado por minuto e oferece cadências mais rápidas para estudo. A demonstração copia a cor de um módulo selecionado como seis caracteres hexadecimais maiúsculos. Uma borda de 2,5 segundos destaca a cor; clicar no círculo receptor cola o código e confirma a correspondência. Origem do código oferece o primeiro módulo, o último ou coordenadas explícitas. A limpeza da área de transferência é tentada após 30 segundos, conforme a permissão do navegador e a conferência do conteúdo atual.

A partir da raiz do repositório:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Abra `http://localhost:8000/examples/`. [Modelo de interação](docs/pt/app-state-flow.md).

## Reprodução do estudo de caso

Python 3.11 ou superior. O ambiente registrado usa Python 3.12.14.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.lock.txt
.venv/bin/pip install --no-deps -e .
make PYTHON=.venv/bin/python test
make PYTHON=.venv/bin/python case-study
```

O [GIF com 16 estados](examples/quad-dimensional-datamatrix-16-states.gif) contém **48 KiB** de payload sintético em uma animação de 256 × 256 pixels. O decoder recupera exatamente o payload hexadecimal original. [Resultados em formato legível por máquina](results/hex-gif-case-study.json).

As verificações de eventos do app podem ser executadas com `make viewer-test` (Node.js).

Os testes também verificam o limite de 64 frames, estados repetidos, ordem da paleta, entrada truncada, módulos inconsistentes, cadência de um frame por minuto, endereços do catálogo e mapeamentos de escalares Unicode.

### Compilar e verificar os PDFs

As duas edições em PDF já estão disponíveis em `paper/`. Para regenerá-las, também são necessários **Pandoc** e **pdfLaTeX (TeX Live)** como ferramentas do sistema, instaladas separadamente das dependências Python. No Ubuntu/Debian:

```bash
sudo apt update
sudo apt install --no-install-recommends pandoc texlive-latex-extra \
  texlive-fonts-recommended texlive-lang-portuguese lmodern poppler-utils
```

Esses pacotes fornecem o conversor de documentos, o compilador LaTeX, os pacotes, as fontes e o suporte ao português. `poppler-utils` fornece `pdftotext` para a verificação do repositório. Consulte o [guia de instalação do Pandoc](https://pandoc.org/installing.html).

Depois, a partir da raiz do repositório, com o ambiente Python preparado acima:

```bash
make PYTHON=.venv/bin/python paper
make PYTHON=.venv/bin/python verify
```

A compilação verifica se `pandoc` e `pdflatex` estão no `PATH` antes de gerar arquivos. Compila os dois idiomas, grava os logs em `output/pdf/` e copia os PDFs resultantes para `paper/`.

Em um checkout Git, a verificação examina os arquivos listados no índice do Git, incluindo novas adições ao staging. Backups locais não versionados, como `.initial/`, ambientes virtuais e arquivos do editor ficam fora dessa varredura. Em um arquivo-fonte distribuído sem metadados Git, a verificação examina os arquivos visíveis e ignora diretórios ocultos e de compilação/cache.

## Discussão e papers

- [Manuscrito em inglês](paper/quad-dimensional-datamatrix.en.md) e [PDF](paper/quad-dimensional-datamatrix.en.pdf).
- [Manuscrito em português](paper/quad-dimensional-datamatrix.pt.md) e [PDF](paper/quad-dimensional-datamatrix.pt.pdf).
- [Questões abertas](docs/pt/discussion.md), incluindo a proposta de relação um a um entre Unicode e hexadecimal.
- [Referências técnicas](docs/pt/technical-references.md).
- [Escopo e limitações](docs/pt/scope-and-limitations.md).

Texto e código são materiais de discussão. Uma etapa posterior poderá propor uma especificação. Os nomes dos autores e o registro de contribuição estão em [CITATION.cff](CITATION.cff). A assistência de implementação e redação por ChatGPT/Codex é reconhecida nos dois papers. O repositório mantém sua [licença](LICENSE).
