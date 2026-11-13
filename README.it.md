<!--
SPDX-FileCopyrightText: 2026 Cecil-IA Labs
SPDX-License-Identifier: MIT
Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
Organization: Cecil-IA Labs
Project: Quad-Dimensional DataMatrix
AI-assisted development: OpenAI ChatGPT and Codex were used as development tools.
Human-directed development and integration. No OpenAI endorsement is implied.
-->
# Quad-Dimensional DataMatrix

**Lingue:** [English](README.md) · [Português (Brasil)](README.pt.md) · [Italiano](README.it.md)

**L'informazione oltre due coordinate.** Il progetto esplora un catalogo logico a quattro coordinate: posizione orizzontale X, posizione verticale Y, dimensione della tavolozza C e stato temporale T. Una sequenza di frame GIF indicizzati costituisce un possibile contenitore digitale.

**[Esplora lo showroom scientifico](https://cecil-ia-labs.github.io/datamatrix-payload/)** · **[Pubblicazione su Zenodo](https://zenodo.org/records/23968974)** · **[Codice sorgente](https://github.com/cecil-ia-labs/datamatrix-payload)**

**Autori:** João Paulo De Luca Jr · Jorge Luiz Espanhol  
**Cecil-IA Labs · Request for Discussion, v0.2.0 · 4 novembre 2026**

## Qual è l'idea?

Nella matrice effettiva 64 × 64, ogni modulo ha le coordinate X e Y. A ogni stato T, un modulo seleziona uno dei valori di una tavolozza con al massimo 64 voci esadecimali. Il profilo di lavoro comprende al massimo 64 frame; ciascun modulo viene rappresentato da un blocco di 4 × 4 pixel nel frame memorizzato da 256 × 256 pixel.

Il catalogo massimo contiene `64⁴ = 16.777.216` **tuple candidate**. Non equivale a 16.777.216 byte di dati: ogni modulo selezionato rappresenta 6 bit con 64 voci. Il profilo massimo contiene 192 KiB di payload grezzo in un ciclo di 64 frame, ovvero 24 KiB/s a una cadenza nominale di 8 frame/s.

## Due esempi distinti

**1. Selezione di uno stato.** L'[applicazione originale](examples/index.html) visualizza 16 stati sintetici pubblici. È possibile scegliere le coordinate di un modulo, mettere in pausa la sequenza, copiare il valore esadecimale corrispondente e provare la ricezione con un cerchio interattivo. Questa esperienza mostra un'interazione locale: non implementa un protocollo di autenticazione verificato.

**2. Trasporto e recupero dei dati.** Il [GIF indicizzato di studio](examples/quad-dimensional-datamatrix-16-states.gif) trasporta 48 KiB di scelte sintetiche distribuite su 16 frame. Il [rapporto riproducibile](results/hex-gif-case-study.json) documenta il recupero esatto dei byte originali. Il GIF di studio non è la registrazione video dell'interfaccia.

Lo showroom integra entrambe le esperienze e permette di ispezionare gli indici e gli indirizzi del catalogo utilizzando i dati effettivi del repository.

## Stato scientifico

Questo lavoro è una **richiesta di discussione** con prototipo e risultati riproducibili. Interoperabilità, robustezza di acquisizione fisica, sicurezza, gestione delle chiavi, framing e correzione degli errori restano oggetto di ricerca.

Consultare i documenti [modello matematico](docs/model.md), [ambito e limitazioni](docs/scope-and-limitations.md) e [flusso degli stati](docs/app-state-flow.md). Le edizioni complete del rapporto sono disponibili in [inglese](paper/quad-dimensional-datamatrix.en.pdf) e [portoghese](paper/quad-dimensional-datamatrix.pt.pdf).

## Reproduzione

Per avviare il visualizzatore e lo showroom da un server locale, dalla radice del repository:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Aprire `http://127.0.0.1:8000/showcase/`. I comandi per riprodurre il caso di studio e verificare i documenti sono nel [README tecnico in inglese](README.md).

## Licenza e attribuzione

Copyright © 2026 Cecil-IA Labs. Licenza [MIT](LICENSE). Si prega di citare entrambi gli autori e la versione archiviata: [DOI 10.5281/zenodo.23968974](https://doi.org/10.5281/zenodo.23968974). Le modifiche assistite da strumenti di IA non implicano affiliazione o approvazione di OpenAI.

Per contributi e sviluppo con agenti: [AGENTS.md](AGENTS.md), [skill del progetto](.agents/skills/).
