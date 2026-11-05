# Quad-Dimensional DataMatrix: preparação do depósito no Zenodo

[English](../publication.md) · [Projeto](../../README.pt.md) · [Notas da versão](release-notes.md)

## Identidade do registro

O objeto principal da pesquisa é o **RfD 0.2.0**, um relatório técnico acompanhado de uma implementação funcional e exemplos reproduzíveis. Prepare um único registro com as duas edições linguísticas e o material de apoio.

| Campo | Valor preparado |
|---|---|
| Título | Quad-Dimensional DataMatrix: Request for Discussion |
| Tipo de recurso | Publication / Report |
| Versão | 0.2.0; tag Git proposta `v0.2.0` |
| Data do relatório | 2026-11-04 |
| Primeiro autor | João Paulo De Luca Jr; sobrenome `De Luca Jr`, nomes `João Paulo` |
| Segundo autor | Jorge Luiz Espanhol; sobrenome `Espanhol`, nomes `Jorge Luiz` |
| Idioma principal | Inglês (`eng`); edição completa em português incluída |
| Editora do relatório | Cecil-IA Labs |
| Acesso | Aberto |
| Licença | MIT, conforme atualmente fornecida no repositório |
| DOI | Omitido até sua reserva ou emissão pelo Zenodo para este objeto |
| Repositório dos fontes | [cecil-ia-labs/datamatrix-payload](https://github.com/cecil-ia-labs/datamatrix-payload) |

Nenhum ORCID, ROR, financiamento ou vínculo institucional individual foi informado nos metadados de citação do projeto. Esses campos opcionais são omitidos. Cecil-IA Labs é a identidade do projeto e da editora do relatório exibida nos manuscritos.

## Arquivos de metadados

- [.zenodo.json](../../.zenodo.json) fornece os metadados do relatório técnico no formato documentado de depósito do Zenodo. A descrição contém um abstract em inglês e um resumo em português. O pacote o copia para `zenodo-metadata.json`; enviar esse JSON apenas como anexo não preenche o formulário web.
- [CITATION.cff](../../CITATION.cff) fornece os dados de citação do GitHub. O tipo superior `software` descreve a implementação; `preferred-citation.type: report` seleciona o RfD como citação acadêmica preferencial. Os dois arquivos registram os mesmos autores e versão.
- As [notas da versão](release-notes.md) descrevem o conteúdo e as evidências da versão preparada.

No arquivamento de releases do GitHub, o Zenodo dá precedência a `.zenodo.json` sobre `CITATION.cff`. Mantenha os arquivos sincronizados. O comando de empacotamento confere título, ordem dos autores, versão, data e licença com os metadados do projeto e do estudo.

## Gerar um pacote para revisão

Com as dependências do [README](../../README.pt.md) instaladas:

```bash
make PYTHON=.venv/bin/python test viewer-test case-study paper verify
# Em um checkout Git, coloque no staging os novos arquivos intencionais da versão.
make PYTHON=.venv/bin/python publication
```

O script inclui os arquivos do índice Git e lê seus bytes atuais na árvore de trabalho. Não coleta arquivos não versionados. Em um arquivo-fonte extraído, usa o manifesto de fontes fornecido. Exclui dados internos do repositório, ambientes locais, caches, saídas de compilação e `.initial/`. Produz:

| Arquivo em `dist/zenodo-v0.2.0/` | Papel no depósito |
|---|---|
| `quad-dimensional-datamatrix.en.pdf` | Relatório técnico em inglês; selecionar como prévia padrão |
| `quad-dimensional-datamatrix.pt.pdf` | Relatório técnico equivalente em português |
| `quad-dimensional-datamatrix-0.2.0-source.zip` | Fontes, figuras, GIF de dados, app, resultados, testes, documentação e as duas gravações de apresentação |
| `quad-dimensional-datamatrix-poc.webm` | Gravação da interface reproduzível separadamente |
| `zenodo-metadata.json` | Campos preparados do registro |
| `release-notes.en.md`, `release-notes.pt.md` | Conteúdo e evidências nos dois idiomas |
| `publication-guide.en.md`, `publication-guide.pt.md` | Cópias das instruções de depósito |
| `source-manifest.json` | Caminhos dos fontes, tamanhos, hashes e origem do commit-base |
| `SHA256SUMS` | Checksums dos demais arquivos da pasta de depósito |

O ZIP externo `dist/quad-dimensional-datamatrix-0.2.0-zenodo.zip` reúne toda a pasta de preparação para download. Extraia-o antes de selecionar os arquivos individuais do depósito. Ele é diferente do arquivo interno dos fontes.

Confira a pasta antes do upload:

```bash
cd dist/zenodo-v0.2.0
sha256sum --check SHA256SUMS
```

O arquivo dos fontes contém o mesmo `source-manifest.json`. Ele identifica o commit-base, se havia diferenças nos arquivos de trabalho no momento do empacotamento e o SHA-256 de cada arquivo incluído. O manifesto dos bytes continua identificando os fontes mesmo quando um commit é feito depois da preparação. Extraia o arquivo dos fontes e execute `make verify` para verificá-lo sem metadados Git; as dependências Python e `pdftotext` precisam estar disponíveis.

## Salvar um rascunho e reservar o DOI

1. Entre no Zenodo e selecione **New upload** no painel.
2. Selecione os dois PDFs, arquivo dos fontes, WebM, notas, metadados, manifesto e checksums da pasta de preparação.
3. Preencha título, tipo de recurso, versão, autores ordenados, idioma, licença, resumo e demais campos a partir de `zenodo-metadata.json`. Preserve os acentos e a ordem dos coautores. A data do relatório é 4 de novembro de 2026; confira se a data de publicação do formulário descreve sua primeira disponibilidade pública real.
4. Marque **No** para DOI existente. Se precisar incluir um DOI nos PDFs antes da publicação, use **Get a DOI now!** e guarde o DOI efetivamente reservado.
5. Salve o rascunho. Selecione o PDF em inglês como prévia padrão, confira os dois relatórios e verifique nomes de arquivos e metadados em Preview.
6. Se houver DOI reservado, inclua-o nas duas edições do manuscrito e nas citações principal e preferencial, regenere os PDFs, reconstrua o pacote e substitua os arquivos do rascunho. Não use um DOI pertencente a outro trabalho.
7. Mantenha o rascunho completo para a decisão de publicação dos autores. O comando de preparação não envia arquivos, reserva identificadores, cria tag Git ou release no GitHub nem publica.

Um DOI reservado é registrado quando o registro é publicado. Não exclua um rascunho cujo DOI já tenha sido inserido nos relatórios. Depois da publicação, copie o DOI efetivo da versão e a URL do registro para os metadados de citação e os links dos READMEs.

## Alternativa pela release do GitHub

A tag proposta é `v0.2.0`. Se o repositório estiver habilitado na integração GitHub do Zenodo, publicar uma release no GitHub dispara o arquivamento. Escolha deliberadamente essa alternativa ou o depósito manual do relatório, para evitar registros duplicados da mesma versão. Uma release em rascunho no GitHub não substitui um depósito completo no Zenodo.

## Orientações oficiais

- [Criar upload, salvar rascunho e reservar DOI](https://help.zenodo.org/docs/deposit/create-new-upload/).
- [Descrição e precedência dos metadados](https://help.zenodo.org/docs/github/describe-software/).
- [Metadados Zenodo JSON](https://help.zenodo.org/docs/github/describe-software/zenodo-json/).
- [Campos da API de metadados de depósito](https://developers.zenodo.org/#deposit-metadata).
- [Arquivar uma release do GitHub](https://help.zenodo.org/docs/github/archive-software/github-upload/).
