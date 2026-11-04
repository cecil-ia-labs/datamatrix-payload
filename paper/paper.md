# datamatrix-payload: capacidade, geometria de cores e transporte visual autenticado

**Juninho De Luca · Cecil-IA Labs**

4 de novembro de 2026 · Manuscrito v0.1 · Circulação privada

[PDF completo com equações numeradas](datamatrix-payload-paper-v0.1.pdf) · [Fonte LaTeX](main.tex) · [BibTeX](references.bib)

## Resumo

Investiga-se a representação de arquivos arbitrários por módulos
coloridos em matrizes visuais. O estudo articula contagem de mensagens,
empacotamento binário, notação hexadecimal, constelações RGB, modelos de
canal, calibração, redundância e confidencialidade. Derivam-se limites
combinatórios e orçamentos finitos que distinguem resolução do arquivo,
número de módulos e dados úteis. Um conjunto anterior de 144 condições
digitais foi reproduzido exatamente. Uma extensão executou 648 quadros
sintéticos em 54 condições, além de 1.000 ensaios de apagamentos com
RS(31,23) sobre GF(32). Demonstrou-se transporte visual simétrico
autenticado de 2.048 bytes, com recuperação exata e rejeição de
modificações de ciphertext, dados associados e chave. Nas simulações com
JPEG Q95 4:2:0, a média de erros de símbolo para 32 cores caiu de 75,56%
com módulos de um pixel para zero observado com módulos de quatro
pixels; esse resultado é condicionado ao pipeline digital e ao
alinhamento utilizados. A análise esclarece por que uma paleta pública é
um mecanismo de representação, enquanto a confidencialidade requer uma
construção criptográfica. A esfera de Bloch estabelece uma associação
geométrica legítima com qubits, sem alterar a natureza clássica do canal
estudado. A contribuição é uma formalização integrada, acompanhada de
evidência computacional auditável e hipóteses para validação óptica
futura.

**Palavras-chave:** comunicação visual; modulação multicolorida;
capacidade; RGB; hexadecimal; Reed–Solomon; criptografia autenticada;
esfera de Bloch.

#### Abstract.

We study arbitrary binary payloads represented by colored modules.
Combinatorial limits, RGB signal geometry, finite-length framing,
erasure coding and authenticated encryption are combined in a
reproducible research framework. An earlier 144-condition digital
benchmark was exactly reproduced. An extension includes 648 synthetic
frames across 54 conditions and 1,000 RS(31,23) erasure trials over
GF(32). A 2,048-byte AES-GCM payload was recovered exactly through a
known-geometry visual channel. Public color mappings, cryptographic
secrecy and quantum-state visualization are formally distinguished.
Results characterize the specified digital simulation; optical capture
and standardized symbology interoperability remain future work.


# Problema, escopo e contribuição

O ponto de partida é uma pergunta operacional: quantos bytes podem ser
recuperados de uma imagem se cada módulo representar uma escolha entre
várias cores? A pergunta depende tanto do conjunto de mensagens
admissíveis quanto do processo físico ou digital que liga emissor e
receptor.

O nome `datamatrix-payload` identifica este projeto. Usa-se *matriz
visual* como termo genérico e *Data Matrix* para a simbologia
padronizada. A implementação experimental não substitui nem implementa a
especificação de QR Code ou JAB Code.

O estudo oferece: (i) orçamento matemático com arredondamento e overhead
explícitos; (ii) conexão entre cores e constelações de comunicação;
(iii) implementação de empacotamento e de RS por avaliação polinomial,
com decodificação de apagamentos; (iv) testes digitais repetíveis; e (v)
uma arquitetura de transporte autenticado. Os elementos teóricos possuem
antecedentes reconhecidos. A contribuição reivindicada nesta versão é
sua integração e a evidência local produzida, sem alegação de prioridade
sobre códigos multicoloridos.

Três níveis de afirmação são empregados: **identidades e limites
matemáticos**, válidos sob hipóteses declaradas; **medições**, que
descrevem execuções concretas; e **hipóteses de engenharia**, cuja
avaliação exige novos experimentos. Em particular, a ausência de erros
em uma simulação finita não determina a confiabilidade de uma câmera.

# Antecedentes técnicos e comparação adequada

QR Code Model 2 possui versões de 21 a 177 módulos por lado; a versão
40-L admite até 2.953 bytes em modo binário. Aumentar sua resolução de
renderização amplia módulos, preservando a estrutura e a capacidade do
símbolo (DENSO WAVE, n.d.).

Para Data Matrix ECC 200, a tabela GS1 distingue 2.335 caracteres
alfanuméricos de 1.556 valores de oito bits no maior símbolo, de
$144\times144$ módulos (GS1 2024). Essa distinção corrige a
identificação anterior de 2.335 como capacidade em bytes.

JAB Code constitui antecedente direto para módulos coloridos. A TR do
BSI especifica construção de paletas e modos de cor; o anexo F inclui a
grade de 32 cores usada neste estudo (Federal Office for Information
Security 2020). ISO/IEC 23634:2022 especifica a simbologia JAB
Code (ISO/IEC 2022). O catálogo confirma a norma; não se presume
conformidade integral deste protótipo com seu texto.

| Sistema                | Unidade de escolha   | Restrição principal                    | Papel neste estudo               |
|:-----------------------|:---------------------|:---------------------------------------|:---------------------------------|
| QR Code                | Módulo binário       | Versões, estruturas e ECC padronizados | Referência de uso e capacidade   |
| Data Matrix ECC 200    | Módulo binário       | Tamanhos e modos padronizados          | Referência de capacidade binária |
| JAB Code               | Módulo colorido      | Protocolo e paletas especificados      | Antecedente técnico direto       |
| Protótipo deste estudo | Índice em paleta RGB | Canal simulado e geometria conhecida   | Instrumento de investigação      |

Comparação conceitual. A capacidade bruta de uma matriz livre não é
equivalente ao payload de uma simbologia completa.

Para um mosaico regular de símbolos com lado $a$ e margem $z$ módulos
por borda, renderizados com lado $s$ pixels por módulo, a contagem
simples é $$T=\left\lfloor\frac{W}{s(a+2z)}\right\rfloor
\left\lfloor\frac{H}{s(a+2z)}\right\rfloor,\qquad B_{\mathrm{mosaico}}=T B_{\text{símbolo}}.$$
Isso contabiliza uma disposição específica, sem otimizar versões,
rotação ou fragmentação. Capacidade agregada também exige índices,
tamanhos e remontagem.

# Capacidade combinatória e tamanho finito

## Do pixel ao módulo

Se uma imagem tem largura $W$ e altura $H$, e cada célula quadrada ocupa
$s\times s$ pixels, o número de posições completas é $$\label{eq:ncells}
N(W,H,s)=\left\lfloor W/s\right\rfloor\left\lfloor H/s\right\rfloor.$$
Aqui $s$ descreve a renderização digital. Em captura óptica, importa
também a quantidade de pixels do sensor que resolve cada célula.

<div class="proposition">

**Proposição 1** (Contagem de mensagens). *Uma matriz de $N$ células
independentes, cada qual livre para assumir um de $q$ símbolos, admite
$q^N$ configurações. Um mapeamento binário injetivo pode representar no
máximo $$\label{eq:counting}
L_{\max}=\left\lfloor N\log_2 q\right\rfloor\ \text{bits}.$$*

</div>

<div class="proof">

*Proof.* O princípio multiplicativo fornece $q^N$ configurações. Para
mapear todas as $2^L$ palavras binárias de comprimento $L$ sem colisões,
exige-se $2^L\le q^N$. Aplicar $\log_2$ e arredondar para baixo produz o
resultado. ◻

</div>

Esta é uma aplicação da medida logarítmica de informação (Shannon 1948),
apresentada como derivação elementar para o projeto.

Se $q=2^b$, cada célula admite exatamente $b$ bits em comprimento fixo.
Se $q$ não é potência de dois, o limite pode ser aproximado por blocos
de $t$ símbolos: $$b_t=\lfloor t\log_2q\rfloor,\qquad
0\le\log_2q-b_t/t<1/t.$$ Portanto $\log_2(129)$ não é um número
fracionário de bits binários independentes atribuível isoladamente a
cada célula por uma tabela de comprimento fixo.

## O caso 8K e o caso 128 por 128

| $q$ | $\log_2q$ | $128\times128$, bytes |    8K, MB |
|----:|----------:|----------------------:|----------:|
|   2 |  1.000000 |               2048.00 |  4.147200 |
|   8 |  3.000000 |               6144.00 | 12.441600 |
|  16 |  4.000000 |               8192.00 | 16.588800 |
|  32 |  5.000000 |              10240.00 | 20.736000 |
|  64 |  6.000000 |              12288.00 | 24.883200 |
| 128 |  7.000000 |              14336.00 | 29.030400 |
| 129 |  7.011227 |              14358.99 | 29.076962 |
| 256 |  8.000000 |              16384.00 | 33.177600 |

Teto ideal com uma célula por pixel e sem overhead. Para 129 estados,
são valores reais de orçamento; bits e bytes inteiros exigem
arredondamento e codificação em blocos.

Para $7680\times4320$, tem-se $N=33.177.600$ quando $s=1$. Com 128
cores, a capacidade ideal é $29.030.400$ bytes. A tabela usa MB
decimais; $1\,\mathrm{MB}=10^6$ bytes e $1\,\mathrm{MiB}=2^{20}$ bytes.

Um módulo que ocupa quatro pixels por lado reduz a quantidade de
posições por fator 16 quando ambas as dimensões são divisíveis por
quatro: $$N(W,H,4)=WH/16.$$ Essa penalidade de área frequentemente
excede o ganho de acrescentar cores. Passar de 32 para 128 cores eleva a
escolha por célula de cinco para sete bits, um fator $7/5=1,4$.

## ASCII, branco, nulidade e preenchimento

ASCII possui 128 valores, incluindo caracteres de controle (Cerf 1969).
Um símbolo dentre 128 escolhas requer sete bits; um byte convencional
reserva oito bits. O canal pode transportar bytes arbitrários em grupos
de cinco ou sete bits, sem depender de texto.

Se branco é um estado extra utilizável livremente, então
$$\Delta b=\log_2(129)-7\simeq0,0112273,\qquad
\frac{\Delta b}{7}\simeq0,00160389.$$ O ganho ideal relativo é apenas
$0,160389\%$. Se branco indicar separação ou padding, ele constitui
overhead e não uma escolha livre adicional. Um branco pertencente à
paleta não cria um 129º estado. O caractere ASCII NUL e a ausência de
conteúdo são conceitos distintos.

## Entropia, compressão e taxa efetiva

Para distribuição marginal $p_i$, a entropia por símbolo é
$$H(X)=-\sum_{i=0}^{q-1}p_i\log_2p_i\le\log_2q.$$ A igualdade vale para
símbolos equiprováveis. Dependência espacial exige analisar sequências;
para um processo estacionário, a taxa de entropia, quando existe, é
$$h_X=\lim_{n\to\infty}\frac{H(X_1,\ldots,X_n)}{n}\le H(X_1).$$ Assim um
arquivo pode ficar abaixo da entropia marginal estimada sem violar o
limite informacional. Compressão explora a estrutura da fonte; mapear os
mesmos bits em cores não comprime o conteúdo por si só.

# Hexadecimal, paletas e representação de imagens

## Uma cor como vetor e como inteiro

A notação CSS `#RRGGBB` expressa três componentes sRGB de oito bits em
seis dígitos hexadecimais (W3C 2026). Para $R,G,B\in\{0,\ldots,255\}$,
$$\label{eq:hex}
u=2^{16}R+2^8G+B,\qquad0\le u<2^{24}.$$ O mapeamento é bijetivo e sua
inversa é $$R=\lfloor u/2^{16}\rfloor,\quad
G=\lfloor u/2^8\rfloor\bmod256,\quad B=u\bmod256.$$ Por exemplo,
$\texttt{0xFF8000}\leftrightarrow(255,128,0)$. A escrita hexadecimal
oferece uma identificação exata dos valores digitais; uma fotografia
desses valores passa por outro canal.

Uma paleta é uma função injetiva
$P:\{0,\ldots,q-1\}\to\{0,\ldots,255\}^3$. Sua representação textual e
seu alfabeto útil têm custos diferentes:
$$\text{descrição RGB de uma entrada}=24\ \text{bits},\qquad
\text{escolha dentre }q\text{ entradas}=\log_2q\ \text{bits}.$$ Com 32
entradas, selecionam-se 32 valores dentre $2^{24}$ possibilidades; a
escolha por módulo tem cinco bits.

Para uma grade cartesiana com $n_R,n_G,n_B$ níveis,
$$q=n_Rn_Gn_B,\quad b=\log_2n_R+\log_2n_G+\log_2n_B,
\quad c_j=\operatorname{round}\left(\frac{255j}{n-1}\right).$$ A grade
$4\times4\times2$ tem $q=32$ e níveis $(0,85,170,255)$ nos dois
primeiros canais e $(0,255)$ no terceiro, seguindo o antecedente
BSI (Federal Office for Information Security 2020).

## Empacotamento e PNG indexado

Índices em $b$ bits para $N$ pixels requerem
$$B_{\text{índices}}=\left\lceil Nb/8\right\rceil,
\qquad B_{\mathrm{paleta}}=3q\ \text{bytes},$$ antes de dimensões,
metadados e compressão. PNG indexado admite profundidades de índice de
1, 2, 4 ou 8 bits (W3C 2025); o formato não define profundidade de cinco
bits. A compressão DEFLATE pode compensar essa representação nominal
mais larga. Por isso deve-se comparar os arquivos efetivamente
produzidos.

## Vetor de índices e imagem vetorial

Serializar índices em ordem de linhas produz um vetor de dados que
permite reconstrução exata. Vetorizar a imagem é representar regiões e
contornos, por exemplo em SVG. Para preservar uma matriz arbitrária, um
SVG pode desenhar retângulos com preenchimento hexadecimal e coordenadas
inteiras. Isso preserva a geometria lógica quando a escala é adequada; a
rasterização ainda pode introduzir mistura de bordas.

Uma paleta de 32 cores não implica 32 regiões conectadas. Se uma imagem
tiver muitas ilhas cromáticas, o número de contornos pode crescer com
$N$, tornando a descrição vetorial maior que o PNG. A escolha entre
índices, regiões e compressão deve ser feita pelo custo medido.

# Cores como constelações de comunicação

## Decisão e distância mínima

Considere os centros de cor $\boldsymbol\mu_i\in\mathbb R^3$, com
$i=0,\ldots,q-1$. Sob ruído gaussiano isotrópico, símbolos equiprováveis
e centros conhecidos, máxima verossimilhança equivale a menor
distância (Forney 2005):
$$\widehat i=\operatorname*{arg\,min}_i\|\mathbf y-\boldsymbol\mu_i\|_2^2,\qquad
d_{\min}=\min_{i\ne j}\|\boldsymbol\mu_i-\boldsymbol\mu_j\|_2.$$

<div class="proposition">

**Proposição 2** (Raio suficiente para decisão correta). *Se
$\mathbf y=\boldsymbol\mu_i+\mathbf e$ e $\|\mathbf e\|_2<d_{\min}/2$, o
detector por menor distância escolhe $i$.*

</div>

<div class="proof">

*Proof.* Para $j\ne i$, a desigualdade triangular fornece
$\|\mathbf y-\boldsymbol\mu_j\|\ge d_{\min}-\|\mathbf e\|>\|\mathbf e\|=\|\mathbf y-\boldsymbol\mu_i\|$. ◻

</div>

O limite é suficiente, não necessário. Na paleta de 32 cores,
$d_{\min}=85$ e o raio suficiente é 42,5 unidades RGB nesse modelo. As
paletas das fotografias têm mínimos de 15,6205 e 19,8242; isso não
estabelece uma ordenação universal de desempenho sob compressão
espacial.

Com covariância comum $\Sigma$, a decisão gaussiana usa
$$D_i=(\mathbf y-\boldsymbol\mu_i)^T\Sigma^{-1}(\mathbf y-\boldsymbol\mu_i)-2\ln p_i.$$
Covariâncias diferentes acrescentam $\ln\det\Sigma_i$ ao critério. A
métrica deve descrever o receptor, em vez de assumir que diferença
numérica sRGB e separação estatística são equivalentes.

No modelo isotrópico ideal, o evento de um concorrente ficar mais
próximo tem probabilidade $Q(d_{ij}/2\sigma)$. Pela união dos eventos,
$$P_e\le\frac1q\sum_i\sum_{j\ne i}Q\left(\frac{d_{ij}}{2\sigma}\right),\qquad
Q(a)=\frac1{\sqrt{2\pi}}\int_a^\infty e^{-u^2/2}\,du.$$ Clipping,
quantização e desfoque presentes nas simulações violam partes desse
modelo. A expressão organiza a análise, sem prever diretamente as taxas
medidas.

## Informação mútua e erros de símbolos

Para probabilidades de transição $T_{ij}=P(\widehat X=j\mid X=i)$ e
distribuição de entrada $p_i$,
$$I(X;\widehat X)=\sum_{i,j}p_iT_{ij}\log_2\frac{T_{ij}}{\sum_kp_kT_{kj}},
\quad C_{\mathrm{dec}}=\max_{\{p_i\}}I(X;\widehat X).$$ O processamento
em decisões discretas pode perder informação da observação contínua:
$I(X;\widehat X)\le I(X;Y)$. A interpretação de capacidade pressupõe um
modelo probabilístico de canal (Shannon 1948).

Como exemplo analítico, para um canal sem memória $q$-ário simétrico,
com erro total $p$ distribuído igualmente entre os $q-1$ símbolos
incorretos, $$C_{\mathrm{sim}}=\log_2q-h_2(p)-p\log_2(q-1),
\quad h_2(p)=-p\log_2p-(1-p)\log_2(1-p).$$ Essa identidade resulta da
entropia condicional de uma linha da matriz de transição. JPEG e
desfoque dependem do entorno; tratá-los como esse canal simétrico seria
uma hipótese adicional.

## Rótulos binários e erros de bits

Uma permutação dos rótulos não altera os pontos RGB, mas pode alterar
quantos bits se perdem em cada confusão. Para rótulos
$\lambda_i\in\{0,1\}^b$,
$$\operatorname{BER}=\frac1b\sum_i p_i\sum_jT_{ij}\,d_H(\lambda_i,\lambda_j).$$
Uma codificação Gray por eixo, $g(v)=v\oplus(v\!\gg\!1)$, é uma hipótese
útil quando confusões entre níveis adjacentes dominam. Ela não foi
comparada experimentalmente nesta versão.

# Canal óptico, amostragem e calibração

Uma câmera integra luz no espaço, no tempo e no espectro. Para canal de
sensor $k$, um modelo radiométrico esquemático é
$$z_k=\int_{\lambda}S_k(\lambda)L(\lambda)\,d\lambda+n_k,$$ onde $S_k$ é
a resposta espectral e $L$ a radiância incidente. O arquivo RGB contém
amostras de uma representação, enquanto a captura mede luz processada
por óptica e sensor.

O modelo agregado usado para organizar hipóteses é $$\label{eq:channel}
\mathbf y_i=\mathcal Q\!\left[g\!\left(\mathbf A\sum_jh_{ij}\mathbf x_j+\mathbf b+\mathbf n_i\right)\right].$$
$h_{ij}$ modela mistura espacial; $\mathbf A$, mistura entre canais;
$\mathbf b$, offsets; $g$, resposta não linear; e $\mathcal Q$,
quantização. Perspectiva e erros de localização exigem ainda uma
transformação geométrica da grade.

Para uma componente sRGB normalizada $c$, a conversão para intensidade
linear tem a forma (W3C 2026)
$$\ell(c)=\begin{cases}c/12,92,&c\le0,04045,\\
((c+0,055)/1,055)^{2,4},&c>0,04045.
\end{cases}$$ Logo intervalos uniformes no valor de código sRGB não são
intervalos uniformes de luz. Ruído gaussiano acrescentado aos códigos
RGB é uma perturbação computacional, não uma caracterização completa do
ruído físico.

A estatística de fótons oferece outra conexão. No modelo de contagem
Poisson, $N_\gamma\sim\mathrm{Poisson}(\mu)$ e (European Machine Vision
Association 2021)
$$\operatorname{Var}(N_\gamma)=\mu,\qquad\mathrm{SNR}_{\mathrm{shot}}=\frac{\mu}{\sqrt\mu}=\sqrt\mu.$$
Com ruído de leitura independente de variância $\sigma_r^2$, uma
expressão simplificada é $\mu/\sqrt{\mu+\sigma_r^2}$. O aumento de área
ou exposição pode elevar $\mu$, limitado por saturação, movimento e
resposta do equipamento.

## Pilotos e ajuste de cor

Se $m$ cores conhecidas são enviadas e medidas, podemos organizar
$Z=[X\ \mathbf1]\in\mathbb R^{m\times4}$ e $Y\in\mathbb R^{m\times3}$.
Para um modelo afim com posto suficiente,
$$\widehat\Theta=\operatorname*{arg\,min}_\Theta\|Z\Theta-Y\|_F^2
=(Z^TZ)^{-1}Z^TY.$$ O inverso explícito ilustra a identidade; uma
implementação numérica deve preferir métodos estáveis como QR ou SVD.
Alternativamente, cada cor piloto recebida pode servir como centro de
decisão, estratégia empregada no benchmark anterior.

A calibração global não corrige automaticamente iluminação variável,
clipping ou mistura espacial dependente do conteúdo. Reservar pilotos
locais aumenta o overhead. Em JPEG 4:2:0, a subamostragem reduz a
resolução cromática (libjpeg-turbo Project, n.d.); mesmo uma paleta bem
separada pode sofrer confusão entre células vizinhas.

# Framing, correção de erros e orçamento útil

## Uma expressão de planejamento

Se $N_d$ células são destinadas ao fluxo codificado, $\eta=N_d/N$ é a
fração estrutural útil e $R=k/n$ a taxa do código, um orçamento
assintótico é $$\label{eq:budget}
B_{\mathrm{dados}}\approx\frac{N\eta R\log_2q}{8}-h,$$ onde $h$ reúne os
bytes do pacote que não pertencem ao conteúdo desejado. Nesta definição
$\eta$ desconta marcadores e pilotos, enquanto $h$ desconta cabeçalhos e
envelope; o mesmo overhead não deve ser subtraído duas vezes.

No exemplo 8K com $s=4$, $q=32$, $\eta=0,9$ e $R=0,8$, o termo anterior
a $h$ é 933.120 bytes. É um cenário de orçamento, não desempenho
validado por câmera.

## RS por avaliação polinomial sobre GF(32)

O alfabeto de cinco bits admite operação sobre $\operatorname{GF}(2^5)$,
construído no protótipo como
$$\operatorname{GF}(32)=\operatorname{GF}(2)[x]/(x^5+x^2+1).$$ O
elemento $\alpha=x$ percorre os 31 elementos não nulos; essa propriedade
é verificada pela implementação. Para mensagem
$\mathbf a=(a_0,\ldots,a_{22})$, define-se
$$f(t)=\sum_{j=0}^{22}a_jt^j,\qquad
\mathbf c=(f(1),f(\alpha),\ldots,f(\alpha^{30})).$$ É uma instância não
sistemática da construção de Reed e Solomon (Reed and Solomon 1960). Se
dois polinômios distintos têm grau máximo 22, sua diferença possui no
máximo 22 raízes. Portanto suas palavras diferem em pelo menos $31-22=9$
posições. O código tem $d_{\min}=9$ e $R=23/31$.

O limite usual de correção é $$\label{eq:rsbound}
2e+v\le n-k=8,$$ com $e$ erros de localização desconhecida e $v$
apagamentos localizados. **O decodificador implementado resolve apenas
apagamentos fornecidos ao programa.** Ele interpola a partir de 23
amostras conhecidas e verifica as demais quando disponíveis. O limite de
quatro erros desconhecidos é propriedade do código, não uma
funcionalidade implementada neste decodificador. Uma referência
operacional distinta é RS(255,223) empregado pelo DSN (Jet Propulsion
Laboratory 2023).

Com exatamente 23 posições consideradas válidas, um erro desconhecido
pode produzir outro polinômio sem inconsistência observável pelo
interpolador. A integridade criptográfica tem função própria na
aceitação final.

## Arredondamentos de pacote e preenchimento

Para pacote de $B$ bytes, símbolos de $b$ bits e blocos RS $(n,k)$,
$$S=\left\lceil\frac{8B}{b}\right\rceil,\quad
J=\left\lceil\frac{S}{k}\right\rceil,\quad
F=nJ,\qquad F\le N_d.$$ O padding deve ser removido usando comprimentos
confiáveis. Na direção inversa, o teto de bytes antes do desconto de
cabeçalhos é $$\label{eq:finite}
B_{\max}=\left\lfloor\frac{bk\lfloor N_d/n\rfloor}{8}\right\rfloor.$$
Para $N_d=128^2$, $b=5$ e RS(31,23), cabem 528 blocos e 7.590 bytes
antes de $h$. Com $h=69$, restam 7.521 bytes. As 16.384 células deste
cálculo são todas de dados; áreas externas de marcadores ou pilotos
devem entrar na área física total.

# Criptografia e paletas: separação formal

## Uma paleta pública é reversível

Considere $C_i=\pi(M_i)$ para uma permutação fixa e pública $\pi$ do
alfabeto.

<div class="proposition">

**Proposição 3** (Reversibilidade da substituição pública). *Conhecer
$C$ e $\pi$ determina $M$; portanto $H(M\mid C,\pi)=0$.*

</div>

<div class="proof">

*Proof.* Como $\pi$ é bijetiva, $M_i=\pi^{-1}(C_i)$ em cada posição. A
distribuição condicional concentra toda a probabilidade numa única
mensagem. ◻

</div>

Mesmo se $\pi$ for secreta, $M_i=M_j$ se e somente se $C_i=C_j$,
revelando padrões. Num ataque de texto escolhido contra uma substituição
fixa independente da posição, uma consulta contendo todos os símbolos
revela a tabela inteira. Para 128 símbolos,
$$|\{\pi\}|=128!,\qquad\log_2(128!)\simeq716,1617.$$ Essa contagem não
corresponde a 716 bits de segurança computacional: o ataque descrito
evita enumerar permutações.

## Máscara secreta e sigilo perfeito

Para mensagens binárias de comprimento $L$, uma máscara $K$ uniforme,
independente, secreta e usada uma única vez fornece $C=M\oplus K$. Para
qualquer $m,c$, $$P(C=c\mid M=m)=P(K=m\oplus c)=2^{-L},
\quad I(M;C)=0.$$ A derivação é um caso de sigilo perfeito no sentido de
Shannon (Shannon 1949). O segredo tem de ser compartilhado previamente,
e o one-time pad isolado não autentica a mensagem. Reutilização expõe
$C_1\oplus C_2=M_1\oplus M_2$. Uma máscara pública não satisfaz a
hipótese de segredo.

## Criptografia autenticada e chave pública

A interface de criptografia autenticada com dados associados é (McGrew
2008) $$(C,T)=\operatorname{AEAD.Enc}_K(\nu,M,A),\qquad
\operatorname{AEAD.Dec}_K(\nu,C,T,A)\in\{M,\bot\}.$$ $\nu$ é o nonce,
$A$ contém contexto autenticado e $\bot$ sinaliza rejeição. AES-GCM
requer gestão correta dos nonces sob cada chave (Dworkin 2007). A
implementação usa a biblioteca `cryptography`, cuja interface rejeita
tags inválidas (Python Cryptographic Authority, n.d.).

Para a proposta cliente–servidor, um esquema de chave pública pode
fornecer o envelope ao receptor. HPKE combina KEM, KDF e AEAD e
constitui uma construção de referência (Barnes et al. 2022). A chave
pública do destinatário pode ser distribuída; sua autenticidade deve ser
estabelecida para evitar substituição por um intermediário. O modo base
não autentica, por si, a identidade do remetente.

O fluxo proposto é compressão do conteúdo, envelope criptográfico,
framing, FEC e mapeamento em cores. O receptor realiza as inversas na
ordem oposta, corrige o canal e só aceita o conteúdo após verificação
criptográfica:
$$I=\operatorname{Render}_{P}\!\left(\operatorname{FEC}\!\left(
\operatorname{Frame}(\operatorname{Encrypt}_{pk}(M))\right)\right).$$
Aqui $\operatorname{Encrypt}_{pk}$ é um esquema completo apropriado;
trocar os rótulos de uma paleta não o implementa. HPKE permanece
proposta arquitetural nesta versão. O teste executado usa AES-GCM
simétrico.

Correção de erros, hash e autenticação têm papéis diferentes. FEC
recupera símbolos sob determinadas condições. SHA-256 no cabeçalho
detecta corrupção acidental, mas um adversário pode recalculá-lo. AEAD
verifica integridade ligada à chave. Replay, remontagem de fragmentos e
autenticação do remetente requerem regras do protocolo.

# Três dimensões, RGB e qubits

## A associação geométrica válida

Um qubit tem espaço de estados $\mathbb C^2$, com bases $|0\rangle$ e
$|1\rangle$. Um estado puro normalizado, a menos de fase global,
escreve-se (IBM Quantum, n.d.a)
$$|\psi\rangle=\cos(\theta/2)|0\rangle+e^{i\phi}\sin(\theta/2)|1\rangle.$$
A representação de Bloch usa
$$\rho=\tfrac12(I+r_x\sigma_x+r_y\sigma_y+r_z\sigma_z),\qquad
\mathbf r=(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta).$$ Para
estados puros, $\|\mathbf r\|_2=1$; estados mistos ocupam
$\|\mathbf r\|_2\le1$. A esfera está embutida em três coordenadas reais,
com dois parâmetros independentes na superfície. As coordenadas são
valores esperados de observáveis; não são três bits acessíveis de forma
independente.

## Uma visualização RGB com precisão finita

Uma transformação convencional para desenhar coordenadas de Bloch é
$$c_k=\operatorname{round}\!\left(\frac{255}{2}(r_k+1)\right),\qquad
\widehat r_k=\frac{2c_k}{255}-1.$$ O arredondamento implica
$|\widehat r_k-r_k|\le1/255$ e
$$\|\widehat{\mathbf r}-\mathbf r\|_2\le\sqrt3/255.$$ Algumas
coordenadas arredondadas podem cair fora da bola. Projetar
$\widehat{\mathbf r}/\max(1,\|\widehat{\mathbf r}\|)$ restaura a
condição geométrica. Essa codificação armazena uma descrição clássica
aproximada de um estado.

## Limite de informação acessível

Para um ensemble de estados de dimensão $d$, a informação clássica
acessível é limitada pela quantidade de Holevo,
$$I_{\mathrm{acc}}\le\chi=S(\bar\rho)-\sum_ip_iS(\rho_i)\le\log_2d,$$
onde $S$ é a entropia de von Neumann (Holevo 1973). Para um qubit
enviado sem emaranhamento previamente compartilhado, $d=2$ dá no máximo
um bit clássico; a codificação superdensa utiliza um recurso adicional
de emaranhamento (IBM Quantum, n.d.b).

Assim a tridimensionalidade do RGB favorece visualização e modelagem de
estados, mas não transforma uma matriz digital em memória quântica. Um
sistema físico com 128 estados mutuamente ortogonais seria de dimensão
128, uma questão diferente da existência de três canais de cor.

# Método experimental e critérios de medição

## Reprodução do benchmark inicial

Os dois arquivos indexados de $64\times64$ e $128\times128$ possuem 32
cores realmente presentes. O primeiro tem 2.148 bytes e o segundo,
7.797. Índices foram empacotados em cinco bits; a reconstrução dos
índices e RGB foi exata. Também se transportaram os arquivos PNG
completos, incluindo seus bytes de metadados, num pacote de 41 bytes de
cabeçalho.

Esse benchmark contém 20 comparações de paletas, 48 testes de
portadoras, quatro testes de calibração e 72 testes de alfabetos: 144
condições digitais. Há ainda 32 cálculos de orçamento. A reexecução
nesta etapa produziu o mesmo JSON de resultados, incluindo métricas e
hashes dos arquivos de referência.

## Extensão sintética

A extensão usa quadros de $64\times64$ símbolos uniformes independentes,
seis alfabetos $q\in\{8,16,32,64,128,256\}$, três lados de módulo
$s\in\{1,2,4\}$ e três perturbações: ruído gaussiano de desvio 16
unidades RGB, JPEG Q95 4:2:0 e desfoque gaussiano de desvio 0,6 pixel.
Cada combinação tem 12 realizações com sementes registradas:
$6\cdot3\cdot3\cdot12=648$ quadros.

O ruído é aplicado por amostra RGB antes da média espacial. A amostragem
usa todos os pixels em módulos de lados um e dois; para lado quatro usa
os quatro pixels centrais. Essa mudança do suporte de amostragem é parte
do detector e deve ser considerada nas comparações. Clipping em
$[0,255]$ e arredondamento são aplicados após as perturbações.

Os testes RS usam 100 mensagens aleatórias para cada quantidade de
apagamentos de zero a nove, totalizando 1.000 blocos. As posições
apagadas são conhecidas e fornecidas ao decodificador; não são estimadas
de fotografias.

No teste criptográfico, uma chave AES-256-GCM e um nonce de 12 bytes são
gerados aleatoriamente apenas em memória. Um payload sintético de 2.048
bytes é cifrado, enquadrado, codificado com RS, renderizado e
recuperado. Nenhuma chave privada é gravada nos artefatos.

## Métricas e incerteza

Com $n_s$ símbolos e rótulos binários de $b$ bits,
$$\widehat{\operatorname{SER}}=\frac{\sum_i\mathbf1[\widehat x_i\ne x_i]}{n_s},\quad
\widehat{\operatorname{BER}}=\frac{\sum_i d_H(\lambda_{\widehat x_i},\lambda_{x_i})}{bn_s}.$$
Considera-se falha de quadro sintético qualquer símbolo incorreto na
ausência de FEC. A taxa estimada é
$$\widehat{\operatorname{PFR}}=\frac{\text{quadros com erro}}{T}.$$ Nos
testes de arquivo, a aceitação exige também igualdade byte a byte. No
teste autenticado, a tag é verificada após recuperar o envelope.

Os CSV registram média e desvio padrão da SER entre quadros. O intervalo
$\bar p\pm t_{0,975,T-1}s_p/\sqrt T$ é uma aproximação para a média
desse ensemble simulado; não garante distribuição normal nem
independência de células. Também se registra limite binomial unilateral
para a probabilidade de falha de quadro sob ensaios independentes de
mesma distribuição. Quando nenhuma das $T$ tentativas falha,
$$\label{eq:zero}
p_{\mathrm{falha},95\%}^{\mathrm{sup}}=1-0,05^{1/T}.$$ Para $T=12$, o
limite é aproximadamente 22,09%. Zero observado em 12 quadros é
evidência finita muito mais fraca que uma garantia de erro inferior a
1%.

# Resultados

## Representação dos arquivos indexados

| Medida                           | $64\times64$ | $128\times128$ |
|:---------------------------------|-------------:|---------------:|
| Pixels                           |         4096 |          16384 |
| Cores presentes                  |           32 |             32 |
| PNG completo, bytes              |         2148 |           7797 |
| Índices de cinco bits, bytes     |         2560 |          10240 |
| Paleta RGB, bytes                |           96 |             96 |
| zlib dos índices + paleta, bytes |         2320 |           8732 |
| Entropia marginal, bits/pixel    |     4.600041 |       4.691384 |
| Distância RGB mínima             |      15.6205 |        19.8242 |

Medidas nos arquivos fornecidos. Cada PNG possui 32 cores; os números
descrevem esses arquivos específicos.

Os PNG completos foram menores que o empacotamento simples com paleta.
Isso é consistente com dependências espaciais aproveitadas pela
compressão. A quantização anterior das imagens não foi revertida nem
avaliada: o alvo de igualdade são os arquivos efetivamente fornecidos.

## Perturbações digitais e tamanho dos módulos

| $q$ | $s$ | Ruído RGB | JPEG 4:2:0 | Desfoque |
|----:|----:|----------:|-----------:|---------:|
|  32 |   1 |     1.243 |     75.564 |   79.842 |
|  32 |   2 |     0.000 |     34.300 |   37.248 |
|  32 |   4 |     0.000 |      0.000 |    0.000 |
| 128 |   1 |    23.116 |     93.764 |   95.302 |
| 128 |   2 |     2.124 |     80.235 |   74.386 |
| 128 |   4 |     2.030 |      0.000 |    0.000 |

SER média, em porcentagem, de 12 quadros por condição. Ruído: desvio 16;
JPEG: Q95; desfoque: desvio 0,6 pixel. Desvios e intervalos completos
constam no CSV.

<figure id="fig:errors">
<embed src="figures/channel-errors.png" />
<figcaption>Média de SER em 12 quadros por condição. O eixo horizontal
varia o alfabeto; cada curva corresponde a um lado de módulo. Os dados
caracterizam o pipeline simulado.</figcaption>
</figure>

Para $q=32$, JPEG95 4:2:0 produz média de 75,56% de erros com $s=1$,
34,30% com $s=2$ e zero observado com $s=4$. Para $q=128$, os valores
correspondentes são 93,76%, 80,23% e zero observado. O resultado de
quatro pixels depende do alinhamento, da média central e do codec
empregado.

Com ruído RGB de desvio 16, a média de SER de $q=128$ permanece em 2,03%
para $s=4$, enquanto $q=32$ apresenta zero observado. Portanto, aumentar
a quantidade de cores pode elevar a densidade nominal e simultaneamente
deteriorar a recuperação.

Os resultados anteriores com as imagens indexadas apresentam
comportamento compatível, mas não idêntico: para JPEG Q95 4:2:0 e $s=1$,
as SER dos dois pacotes são 72,91% e 74,13%. O conteúdo dos símbolos e o
framing diferem do ensemble sintético uniforme.

## Calibração no benchmark anterior

Sob mistura afim global de canais, offsets e ruído de desvio três, o
detector nominal apresentou 17,19% e 17,37% de erros. Ao usar os pilotos
recebidos como centros, os dois arquivos foram recuperados exatamente.
São dois casos com geometria conhecida e transformação compartilhada por
pilotos e conteúdo; o teste não representa calibração local em uma
câmera real.

## Apagamentos RS e transporte autenticado

| Apagamentos | Ensaios | Recuperados | Recusados |
|------------:|--------:|------------:|----------:|
|           0 |     100 |         100 |         0 |
|           1 |     100 |         100 |         0 |
|           2 |     100 |         100 |         0 |
|           3 |     100 |         100 |         0 |
|           4 |     100 |         100 |         0 |
|           5 |     100 |         100 |         0 |
|           6 |     100 |         100 |         0 |
|           7 |     100 |         100 |         0 |
|           8 |     100 |         100 |         0 |
|           9 |     100 |           0 |       100 |

RS(31,23) por avaliação em GF(32). As posições dos apagamentos são
fornecidas ao interpolador; não há localização de erros desconhecidos.

Todos os 900 blocos com até oito apagamentos foram reconstruídos
exatamente; os 100 blocos com nove foram recusados. Nenhuma reconstrução
incorreta foi observada nesses ensaios. A verificação é compatível com a
distância mínima derivada para a construção utilizada.

O pacote autenticado possui 2.117 bytes: 2.048 de conteúdo, 12 de nonce,
16 de tag e 41 de cabeçalho experimental. São 3.388 símbolos antes de
FEC, preenchidos para 148 blocos RS e 4.588 módulos codificados. O canal
visual sem perturbação recuperou o conteúdo exatamente. As três
tentativas negativas, com ciphertext modificado, AAD modificado e chave
diferente, produziram rejeição da tag.

O teste confirma o encadeamento executado; não é uma prova nova da
segurança de AES-GCM. A injeção de erros desconhecidos em um canal
óptico e a recuperação conjunta de FEC e AEAD ainda não foram medidas.

<figure>
<embed src="figures/constellation-capacity.png" />
<figcaption>À esquerda, os 32 pontos da constelação RGB. À direita, teto
combinatório em 8K antes de overhead e erro de canal. A densidade cresce
com <span class="math inline">log<sub>2</sub><em>q</em></span> e cai
aproximadamente com <span
class="math inline"><em>s</em><sup>2</sup></span>.</figcaption>
</figure>

# Discussão: otimizar bytes recuperados

A métrica de engenharia relevante combina orçamento e aceitação. Para
área renderizada $A_{\mathrm{px}}$ e duração $\tau$, define-se
$$G_A=\frac{8B_{\mathrm{payload}}(1-\operatorname{PFR})}{A_{\mathrm{px}}},\qquad
G_t=\frac{8B_{\mathrm{payload}}(1-\operatorname{PFR})}{\tau}.$$ São bits
úteis esperados por pixel renderizado e por segundo, respectivamente.
Não se equipara automaticamente pixel renderizado a área física ou pixel
de câmera.

O problema de projeto pode ser escrito como
$$(q,s,R,\eta,P)^*=\operatorname*{arg\,max}_{\mathcal D}G_A
\quad\text{sujeito a}\quad\operatorname{PFR}\le\varepsilon,$$ onde
$\mathcal D$ representa escolhas admissíveis de alfabeto, geometria,
código e calibração no canal medido. A restrição de confiabilidade evita
premiar densidade nominal com recuperação insuficiente.

Há duas observações de projeto. Primeiro, a paleta que aproxima uma
fotografia pode ser inadequada como constelação de transporte; fonte e
canal têm objetivos distintos. Segundo, ciphertext bem construído se
aproxima de dados de alta entropia e tende a remover correlações úteis
para compressão da portadora. Comprimir o conteúdo antes de cifrar é uma
escolha coerente para arquivos independentes; o tamanho final deve ser
medido. Esse estudo não avalia vazamentos por comprimento em protocolos
interativos.

# Hipóteses e plano de validação óptica

1.  **Calibração local:** pilotos por região podem aumentar a
    recuperação sob iluminação não uniforme, desde que o ganho compense
    a área consumida.

2.  **Rótulos e BER:** Gray por eixo pode reduzir BER quando confusões
    adjacentes dominam, mesmo com SER semelhante.

3.  **Apagamentos por confiança:** usar distância ao primeiro e segundo
    centros para sinalizar células ambíguas pode aproveitar o orçamento
    $2e+v\le8$ melhor que decisões sempre forçadas.

4.  **Interleaving:** distribuir células entre blocos pode aumentar a
    tolerância a regiões desfocadas ou obstruídas. A vantagem depende da
    distribuição espacial dos erros.

5.  **Escolha adaptativa:** a configuração que maximiza $G_A$ pode
    variar com distância, foco, exposição, codec e aparelho.

Um ensaio futuro deve registrar dispositivo emissor e receptor,
resolução de captura, distância, ângulo, exposição, iluminação, foco,
formato e parâmetros de processamento. Devem ser guardados captura bruta
disponível, imagem processada, configuração e referência de bytes. A
separação entre conjuntos de calibração e teste evita ajustar o receptor
ao mesmo quadro usado para avaliar desempenho.

É necessário comparar com leitores e geradores padronizados em condições
equivalentes de área e taxa de falha. O presente trabalho não executou
um benchmark de desempenho contra JAB Code. A comparação atual é
conceitual e de orçamento.

Para planejar a quantidade de ensaios com zero falhas e limite
unilateral $\alpha$, a
Eq. <a href="#eq:zero" data-reference-type="eqref"
data-reference="eq:zero">[eq:zero]</a> implica
$$T\ge\left\lceil\frac{\ln\alpha}{\ln(1-\varepsilon)}\right\rceil.$$
Para $\alpha=0,05$ e $\varepsilon=10^{-3}$, são necessárias pelo menos
2.995 tentativas independentes da distribuição que se pretende
caracterizar, todas sem falha. Alterar a distribuição de aparelhos ou
condições altera o alcance da inferência.

# Limitações e conclusão

Todas as medições são digitais. A geometria e o alinhamento são
conhecidos, e as constelações não foram otimizadas para um sensor
particular. Os resultados de JPEG dependem da implementação e do
posicionamento dos blocos. O benchmark de imagens usa dois arquivos; a
extensão usa padrões sintéticos uniformes. A extensão RS lida com
apagamentos fornecidos, não com localização automática de erros. A
demonstração criptográfica é simétrica e não implementa HPKE. Ausência
de erros observados não estabelece risco zero.

A análise estabelece uma base matemática e experimental consistente para
matrizes multicoloridas. A identidade hexadecimal permite manipular
cores como valores digitais exatos; a capacidade útil depende da escolha
do alfabeto, do canal e da redundância. Paletas públicas podem
transportar ciphertext, preservando a separação entre representação e
segredo. A associação 3D com qubits é válida para descrever estados,
enquanto a matriz continua sendo um meio clássico. A próxima
contribuição verificável será medir a recuperação óptica e comparar
escolhas de projeto sob um mesmo orçamento de área e confiabilidade.

# Autoria, assistência e proveniência

Concepção da investigação, perguntas e direção do projeto: Juninho De
Luca. A organização do texto, a implementação e a execução dos
experimentos desta versão tiveram assistência de ChatGPT/Codex, da
OpenAI. Fórmulas padrão são atribuídas à literatura; aplicações, provas
elementares e resultados computacionais são identificados no corpo do
texto. O manuscrito está sujeito à revisão do autor antes de submissão
ou divulgação pública. Não há alegação de revisão por pares ou validação
institucional.

# Notação e inventário de evidência

| Símbolo                                                    | Significado                                                           |
|:-----------------------------------------------------------|:----------------------------------------------------------------------|
| $W,H$                                                      | Dimensões em pixels da renderização considerada.                      |
| $s$                                                        | Lado do módulo, em pixels renderizados.                               |
| $N,N_d$                                                    | Número de células completas e número reservado ao fluxo codificado.   |
| $q,b$                                                      | Quantidade de estados e bits por símbolo para $q=2^b$.                |
| $\eta,R,h$                                                 | Fração estrutural útil, taxa do código e overhead em bytes de pacote. |
| $P,\mathcal P$                                             | Mapeamento índice–cor e constelação de centros RGB.                   |
| $e,v$                                                      | Erros desconhecidos e apagamentos localizados por bloco.              |
| $\nu,A$                                                    | Nonce e dados associados da interface AEAD.                           |
| $\operatorname{SER},\operatorname{BER},\operatorname{PFR}$ | Taxas de erro de símbolo, bit e falha de quadro.                      |

`results/baseline/` contém métricas anteriores; `results/extended/`
contém os 648 ensaios, estatísticas agregadas, testes RS, parâmetros de
ambiente e resultados de integridade. `paper/tables/` é gerado desses
JSON. `tests/` verifica comportamentos de empacotamento, hexadecimal,
leitura exata, apagamentos e rejeição de inconsistências. As duas
imagens pessoais permanecem como fixtures externas opcionais,
identificadas por nome e SHA-256; o conjunto sintético reproduzível não
depende delas.

# Reprodução computacional

Ambiente registrado: Python 3.12.14, NumPy 2.3.5, Pillow 13.0.0, SciPy
1.17.0, Matplotlib 3.10.8 e cryptography 50.0.2. A semente-base é
20261104. O encoder JPEG é aquele disponível no Pillow desse ambiente;
sua versão é registrada no arquivo de ambiente complementar.

Instalar as dependências do projeto e executar:

    PYTHONPATH=src python3 -m unittest discover -s tests -v
    python3 experiments/extended.py
    python3 experiments/build_tables.py
    make paper

O benchmark com os arquivos originais é opcional e aceita `–inputs` e
`–out`. Os hashes permitem conferir a identidade dessas entradas. Os
resultados estocásticos de canal são determinados pelas sementes e pelo
ambiente; as chaves e os nonces do teste AES-GCM são novos a cada
execução, preservando as mesmas propriedades e tamanhos, sem gravar
segredos.

# Referências

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-2022barnesHpke" class="csl-entry">

Barnes, Richard, Karthikeyan Bhargavan, Benjamin Lipp, and Christopher
Wood. 2022. “Hybrid Public Key Encryption.” RFC 9180. RFC Editor.
<https://doi.org/10.17487/RFC9180>.

</div>

<div id="ref-1969cerfAscii" class="csl-entry">

Cerf, Vint. 1969. “<span class="nocase">ASCII format for Network
Interchange</span>.” RFC 20. RFC Editor.
<https://doi.org/10.17487/RFC0020>.

</div>

<div id="ref-densoVersions" class="csl-entry">

DENSO WAVE. n.d. “Information Capacity and Versions of QR Code.”
<https://www.qrcode.com/en/about/standards.html>.

</div>

<div id="ref-2007nistGcm" class="csl-entry">

Dworkin, Morris. 2007. “Recommendation for Block Cipher Modes of
Operation: Galois/Counter Mode (GCM) and GMAC.” SP 800-38D. NIST.
<https://doi.org/10.6028/NIST.SP.800-38D>.

</div>

<div id="ref-2021emvaLinear" class="csl-entry">

European Machine Vision Association. 2021. *EMVA Standard 1288, Release
4.0 Linear*. EMVA.
<https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf>.

</div>

<div id="ref-2020bsiJab" class="csl-entry">

Federal Office for Information Security. 2020. *BSI TR-03137 Part 2: JAB
Code Color Bar Code Symbology Specification*. BSI.
<https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03137/BSI-TR-03137_Part2.pdf>.

</div>

<div id="ref-2005forneySignals" class="csl-entry">

Forney, G. David. 2005. “Performance of Small Signal Sets.” MIT
OpenCourseWare, Principles of Digital Communication II, Chapter 5.
<https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/9c669af76ebf74ffe46645541f1ff6b3_chap_5.pdf>.

</div>

<div id="ref-2024gs1General" class="csl-entry">

GS1. 2024. *GS1 General Specifications*. GS1 AISBL.
<https://ref.gs1.org/standards/genspecs/24.0.0/>.

</div>

<div id="ref-1973holevoBounds" class="csl-entry">

Holevo, A. S. 1973. “Bounds for the Quantity of Information Transmitted
by a Quantum Communication Channel.” *Problems of Information
Transmission* 9 (3): 177–83. <https://www.mathnet.ru/eng/ppi903>.

</div>

<div id="ref-ibmBloch" class="csl-entry">

IBM Quantum. n.d.a. “Bloch Sphere.” IBM Quantum Learning.
<https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/density-matrices/bloch-sphere>.

</div>

<div id="ref-ibmSuperdense" class="csl-entry">

———. n.d.b. “Superdense Coding.” IBM Quantum Learning.
<https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/superdense-coding>.

</div>

<div id="ref-2022isoJab" class="csl-entry">

ISO/IEC. 2022. *<span class="nocase">ISO/IEC 23634:2022: JAB Code
polychrome bar code symbology specification</span>*. ISO.
<https://webstore.iec.ch/en/publication/75648>.

</div>

<div id="ref-2023jplTelemetry" class="csl-entry">

Jet Propulsion Laboratory. 2023. *Telemetry General Information*.
California Institute of Technology.
<https://deepspace.jpl.nasa.gov/dsndocs/810-005/206/206E.pdf>.

</div>

<div id="ref-libjpegUsage" class="csl-entry">

libjpeg-turbo Project. n.d. “<span class="nocase">libjpeg-turbo usage
documentation</span>.”
<https://github.com/libjpeg-turbo/libjpeg-turbo/blob/main/doc/usage.txt>.

</div>

<div id="ref-2008mcgrewAead" class="csl-entry">

McGrew, David. 2008. “An Interface and Algorithms for Authenticated
Encryption.” RFC 5116. RFC Editor. <https://doi.org/10.17487/RFC5116>.

</div>

<div id="ref-pycaAead" class="csl-entry">

Python Cryptographic Authority. n.d. “Authenticated Encryption.”
<https://cryptography.io/en/stable/hazmat/primitives/aead/>.

</div>

<div id="ref-1960reedPolynomial" class="csl-entry">

Reed, I. S., and G. Solomon. 1960. “Polynomial Codes over Certain Finite
Fields.” *Journal of the Society for Industrial and Applied Mathematics*
8 (2): 300–304. <https://doi.org/10.1137/0108018>.

</div>

<div id="ref-1948shannonCommunication" class="csl-entry">

Shannon, Claude E. 1948. “A Mathematical Theory of Communication.” *The
Bell System Technical Journal* 27: 379–423, 623–56.
<https://doi.org/10.1002/j.1538-7305.1948.tb01338.x>.

</div>

<div id="ref-1949shannonSecrecy" class="csl-entry">

———. 1949. “Communication Theory of Secrecy Systems.” *The Bell System
Technical Journal* 28 (4): 656–715.
<https://doi.org/10.1002/j.1538-7305.1949.tb00928.x>.

</div>

<div id="ref-2025w3cPng" class="csl-entry">

W3C. 2025. *Portable Network Graphics (PNG) Specification, Third
Edition*. World Wide Web Consortium.
<https://www.w3.org/TR/2025/REC-png-3-20250624/>.

</div>

<div id="ref-2026w3cColor" class="csl-entry">

———. 2026. *CSS Color Module Level 4*. World Wide Web Consortium.
<https://www.w3.org/TR/2026/CRD-css-color-4-20261103/>.

</div>

</div>
