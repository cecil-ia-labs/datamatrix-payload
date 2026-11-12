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

# Quad-Dimensional DataMatrix: mathematical model

[Português](pt/model.md) · [Scope and Limitations](scope-and-limitations.md)

## Four-coordinate catalogue

Let $W=H=64$, $F\le64$, and $K\le64$. Coordinates are horizontal position $x$, vertical position $y$, temporal state $t$, and dimension identifier $d$:

$$\Omega=\{0,\ldots,W-1\}\times\{0,\ldots,H-1\}\times\{0,\ldots,F-1\}\times\{0,\ldots,K-1\}.$$

The maximum catalogue contains $|\Omega|=WHFK=64^4=16{,}777{,}216$ candidate tuples. A dense state selects one dimension per position:

$$D[t,y,x]\in\{0,\ldots,K-1\},\qquad A[t,y,x,d]=\mathbf1_{\{D[t,y,x]=d\}}.$$

Thus $\sum_d A[t,y,x,d]=1$. The four-index indicator tensor describes the same data as the three-index array of dimension choices.

For the maximum profile, a candidate address can be packed as

$$a=(((64t+y)64+x)64+d),\qquad 0\le a\le\mathtt{0xFFFFFF}.$$

Each coordinate occupies six bits. The prototype exposes hexadecimal catalogue addresses.

## Selected data and rate

There are $N=WHF$ selected modules and $K^N$ unrestricted dense sequences. The binary counting bound is

$$L_{\max}=\lfloor WHF\log_2K\rfloor.$$

For $K=64$, each module represents six bits. At the maximum profile:

$$N=262{,}144,\quad L_{\max}=1{,}572{,}864\text{ bits},\quad B_{\max}=196{,}608\text{ bytes}=192\text{ KiB}.$$

At $f=8$ states per second, $T=F/f=8$ seconds:

$$R_{\Omega}=|\Omega|/T=2{,}097{,}152\text{ candidate tuples/s},$$
$$R_{\mathrm{modules}}=WHf=32{,}768\text{ modules/s},$$
$$R_{\mathrm{bits}}=WHf\log_2K=196{,}608\text{ bits/s}=24\text{ KiB/s}.$$

If “cps” is used in this discussion, it denotes **candidate tuples per second**. It does not denote characters, bytes, or accepted authentication codes per second.

## Hexadecimal palette

$P_t(d)$ is a six-digit hexadecimal entry, for example $\mathtt{0x12ABEF}$. The current palette contains at most 64 entries selected from $2^{24}$ possible hexadecimal values. Each module stores its palette index; the table supplies the corresponding value. A palette is a codebook.

The stored image repeats each effective index across a $4\times4$ block. A frame has $256^2$ stored pixels and $64^2$ independent modules. Changing the repeated pixel count preserves the number of independent choices.

## Unicode discussion candidates

Unicode scalar values occupy $\mathtt{0x000000}$ through $\mathtt{0x10FFFF}$, excluding $\mathtt{0x00D800}$ through $\mathtt{0x00DFFF}$. There are

$$0x110000-0x800=1{,}112{,}064$$

scalar values. UTF-8 represents them using one to four octets.

One direct mapping is $h(u)=\mathrm{hex}_6(u)$. It is injective because equal six-digit hexadecimal values imply equal integers. In a frame with at most 64 active entries, a direct palette dictionary can name at most 64 distinct scalar values simultaneously.

A second candidate represents a scalar with four six-bit dimension identifiers:

$$u=64^3d_0+64^2d_1+64d_2+d_3.$$

This accommodates every scalar value because $0x10FFFF<64^4$. The prototype supplies both reversible helper mappings as discussion tools. The paper also discusses mapping a scalar to a catalogue address.

Primary references: [GIF89a](https://www.w3.org/Graphics/GIF/spec-gif89a.txt), [Unicode §3.9](https://www.unicode.org/versions/Unicode18.0.0/core-spec/chapter-3/), [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html).

## Reproducible evidence

The distributed study selects `F=16` and `K=64`: 65,536 effective modules carry 393,216 bits, or 48 KiB. Its stored cycle is two seconds at 8 fps. The [results](../results/hex-gif-case-study.json) and [release notes](release-notes.md) identify the exact GIF and recovered payload. [Archive preparation](publication.md) preserves this evidence with the two language editions.
