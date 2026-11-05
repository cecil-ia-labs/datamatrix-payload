# Quad-Dimensional DataMatrix: modelo matemático

[English](../model.md) · [Escopo e limitações](scope-and-limitations.md)

## Catálogo de quatro coordenadas

Sejam $W=H=64$, $F\le64$ e $K\le64$. As coordenadas são posição horizontal $x$, posição vertical $y$, estado temporal $t$ e identificador de dimension $d$:

$$\Omega=\{0,\ldots,W-1\}\times\{0,\ldots,H-1\}\times\{0,\ldots,F-1\}\times\{0,\ldots,K-1\}.$$

O catálogo máximo contém $|\Omega|=WHFK=64^4=16.777.216$ tuplas candidatas. Um estado denso seleciona uma dimension por posição:

$$D[t,y,x]\in\{0,\ldots,K-1\},\qquad A[t,y,x,d]=\mathbf1_{\{D[t,y,x]=d\}}.$$

Portanto, $\sum_d A[t,y,x,d]=1$. O tensor indicador de quatro índices descreve os mesmos dados que o array de três índices das escolhas de dimension.

Para o perfil máximo, um endereço candidato pode ser empacotado como

$$a=(((64t+y)64+x)64+d),\qquad 0\le a\le\mathtt{0xFFFFFF}.$$

Cada coordenada ocupa seis bits. O protótipo expõe endereços hexadecimais do catálogo.

## Dados selecionados e taxa

Há $N=WHF$ módulos selecionados e $K^N$ sequências densas sem restrições. O limite de contagem binária é

$$L_{\max}=\lfloor WHF\log_2K\rfloor.$$

Com $K=64$, cada módulo representa seis bits. No perfil máximo:

$$N=262.144,\quad L_{\max}=1.572.864\text{ bits},\quad B_{\max}=196.608\text{ bytes}=192\text{ KiB}.$$

Para $f=8$ estados por segundo, $T=F/f=8$ segundos:

$$R_{\Omega}=|\Omega|/T=2.097.152\text{ tuplas candidatas/s},$$
$$R_{\mathrm{modules}}=WHf=32.768\text{ módulos/s},$$
$$R_{\mathrm{bits}}=WHf\log_2K=196.608\text{ bits/s}=24\text{ KiB/s}.$$

Se “cps” for empregado nesta discussão, designará **tuplas candidatas por segundo**. Não designa caracteres, bytes nem códigos de autenticação aceitos por segundo.

## Paleta hexadecimal

$P_t(d)$ é uma entrada hexadecimal de seis dígitos, por exemplo $\mathtt{\#12ABEF}$. A paleta atual contém até 64 entradas escolhidas entre $2^{24}$ valores hexadecimais possíveis. Cada módulo armazena seu índice na paleta; a tabela fornece o valor correspondente. A paleta é um dicionário de código.

A imagem armazenada repete cada índice efetivo em um bloco de $4\times4$. Um frame possui $256^2$ pixels armazenados e $64^2$ módulos independentes. Alterar a quantidade de pixels repetidos preserva a quantidade de escolhas independentes.

## Candidatos à discussão sobre Unicode

Os escalares Unicode ocupam de $\mathtt{0x000000}$ a $\mathtt{0x10FFFF}$, excluindo de $\mathtt{0x00D800}$ a $\mathtt{0x00DFFF}$. Existem

$$0x110000-0x800=1.112.064$$

valores escalares. UTF-8 os representa usando de um a quatro octetos.

Um mapeamento direto é $h(u)=\mathrm{hex}_6(u)$. É injetivo, pois valores hexadecimais de seis dígitos iguais implicam inteiros iguais. Em um frame com até 64 entradas ativas, um dicionário direto de paleta pode nomear até 64 escalares distintos simultaneamente.

Um segundo candidato representa um escalar por quatro identificadores de dimension de seis bits:

$$u=64^3d_0+64^2d_1+64d_2+d_3.$$

Isso acomoda todos os escalares porque $0x10FFFF<64^4$. O protótipo oferece as duas funções reversíveis como instrumentos de discussão. O paper também discute o mapeamento de um escalar para um endereço do catálogo.

Referências primárias: [GIF89a](https://www.w3.org/Graphics/GIF/spec-gif89a.txt), [Unicode §3.9](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-3/), [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html).

## Evidência reproduzível

O estudo distribuído usa `F=16` e `K=64`: 65.536 módulos efetivos transportam 393.216 bits, ou 48 KiB. Seu ciclo armazenado dura dois segundos a 8 fps. Os [resultados](../../results/hex-gif-case-study.json) e as [notas da versão](release-notes.md) identificam o GIF exato e o payload recuperado. A [preparação do arquivamento](publication.md) preserva essas evidências junto com as duas edições linguísticas.
