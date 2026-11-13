/*
 * SPDX-FileCopyrightText: 2026 Cecil-IA Labs
 * SPDX-License-Identifier: MIT
 * Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
 * Organization: Cecil-IA Labs
 * Project: Quad-Dimensional DataMatrix
 * AI-assisted development: OpenAI ChatGPT and Codex were used as development tools.
 * Human-directed development and integration. No OpenAI endorsement is implied.
 */
'use strict';
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('showcase/index.html'),css=read('showcase/showroom.css'),js=read('showcase/showroom.js');
test('research metadata, authors and archive',()=>{
 assert.match(html,/João Paulo De Luca Jr/);
 assert.match(html,/Jorge Luiz Espanhol/);
 assert.match(html,/zenodo\.org\/records\/23968974/);
 assert.match(html,/rel="canonical"/);
});
test('real dataset is connected to original viewer without duplicate payload files',()=>{
 assert.match(html,/id="matrix"/);
 assert.match(html,/id="original-viewer"/);
 assert.match(js,/import\(new URL\('state-data\.js',exampleUrl\)\.href\)/);
 assert.match(js,/module_indices_hex/);
 assert.match(js,/palette_hex/);
 assert.match(js,/examples\//);
 assert.ok(fs.existsSync(path.join(root,'examples/state-data.js')));
 assert.ok(fs.existsSync(path.join(root,'examples/quad-dimensional-datamatrix-16-states.gif')));
});
test('scientific quantities match reproducible report',()=>{
 const report=JSON.parse(read('results/hex-gif-case-study.json'));
 assert.equal(report.case_study.frames,16);
 assert.equal(report.case_study.payload_bytes,49152);
 assert.equal(report.case_study.exact_recovery,true);
 assert.equal(report.catalogue.full_tuple_count,16777216);
 assert.match(html,/candidate tuples/);
 assert.match(html,/not a validated authentication credential/);
});
test('static source remains responsive and deployment stays manual',()=>{
 assert.match(css,/@media\(max-width:740px\)/);
 assert.match(css,/\[hidden\]\{display:none!important\}/);
 const flow=read('.github/workflows/publish-showcase.yml');
 assert.match(flow,/workflow_dispatch:/);
 assert.doesNotMatch(flow,/^\s*push:/m);
 assert.match(flow,/node tests\/test_viewer\.cjs/);
});
