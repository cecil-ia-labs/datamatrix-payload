/*
 * SPDX-FileCopyrightText: 2026 Cecil-IA Labs
 * SPDX-License-Identifier: MIT
 * Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
 * Organization: Cecil-IA Labs
 * Project: Quad-Dimensional DataMatrix
 * AI-assisted development: OpenAI ChatGPT and Codex were used as development tools.
 * Human-directed development and integration. No OpenAI endorsement is implied.
 */
// Self-contained research-page controls. The real 16-state data are loaded on request.
const byId=id=>document.getElementById(id);
const canvas=byId('matrix'),ctx=canvas.getContext('2d',{alpha:false});
let states=null,frame=0,x=0,y=0,timer=null;
const base=new URL('.',import.meta.url);
const development=base.pathname.endsWith('/showcase/');
const exampleUrl=new URL(development?'../examples/':'./examples/',base);
const palette=['#0c566d','#24768a','#399ca9','#58c6be','#c597d4','#ae8dec','#fe9c89','#356386','#55a1d3','#9fdbcb','#d6b0f9','#eec89b'];
let s=20261104;const rnd=()=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return s/4294967296;};
const art=byId('hero-art');
for(let i=0;i<144;i++){const tile=document.createElement('i');tile.style.setProperty('--pixel',palette[Math.floor(rnd()*palette.length)]);tile.style.setProperty('--opacity',String(.25+rnd()*.75));art.append(tile);}
const clamp=(n)=>Number.isFinite(n)?Math.min(63,Math.max(0,Math.trunc(n))):0;
function dimensionAt(state,px,py){const pos=2*(py*64+px);return Number.parseInt(state.module_indices_hex.slice(pos,pos+2),16);}
function displayCoordinate(){
 if(!states)return;
 const state=states[frame],dimension=dimensionAt(state,x,y),color=state.palette_hex[dimension];
 const address=(((frame*64+y)*64+x)*64+dimension).toString(16).toUpperCase().padStart(6,'0');
 byId('x').value=String(x);byId('y').value=String(y);
 byId('hex').textContent=color?.toUpperCase()??'—';
 byId('color-sample').style.backgroundColor=color??'#213f4b';
 byId('dimension').textContent=String(dimension);
 byId('state-readout').textContent=String(frame)+' of '+states.length;
 byId('address').textContent='0x'+address;
 byId('frame-indicator').textContent='STATE '+(frame+1)+' / '+states.length;
 byId('t-output').textContent=String(frame);
}
function draw(){
 if(!states)return;
 const state=states[frame];
 for(let yy=0;yy<64;yy++){
  for(let xx=0;xx<64;xx++){
   const dimension=dimensionAt(state,xx,yy);
   ctx.fillStyle=state.palette_hex[dimension];
   ctx.fillRect(xx,yy,1,1);
  }
 }
 byId('frame').value=String(frame);
 displayCoordinate();
}
function go(target){if(!states)return;frame=(target+states.length)%states.length;draw();}
function stop(){if(timer!==null){clearInterval(timer);timer=null;}byId('play').textContent='Play';}
function toggle(){
 if(!states)return;
 if(timer!==null){stop();return;}
 byId('play').textContent='Pause';
 timer=setInterval(()=>go(frame+1),125);
}
byId('load-study').addEventListener('click',async()=>{
 const button=byId('load-study');button.disabled=true;button.textContent='Loading original states…';
 try{
  const data=await import(new URL('state-data.js',exampleUrl).href);
  if(!Array.isArray(data.states)||data.states.length!==16||data.states.some(state=>state.module_indices_hex?.length!==8192||state.palette_hex?.length!==64))throw Error('Unexpected study structure');
  states=data.states;byId('grid-loading').hidden=true;
  for(const id of ['previous','next','frame','play','x','y'])byId(id).disabled=false;
  button.textContent='Original dataset loaded ✓';draw();
 }catch(err){
  button.disabled=false;button.textContent='Try loading the study again';
  byId('grid-loading').textContent='Dataset unavailable. Serve the repository with a local web server or use the published Pages site.';
  console.error('Study load failed',err);
 }
});
byId('frame').addEventListener('input',event=>{stop();go(Number(event.target.value));});
byId('previous').addEventListener('click',()=>{stop();go(frame-1);});
byId('next').addEventListener('click',()=>{stop();go(frame+1);});
byId('play').addEventListener('click',toggle);
byId('x').addEventListener('input',event=>{x=clamp(Number(event.target.value));displayCoordinate();});
byId('y').addEventListener('input',event=>{y=clamp(Number(event.target.value));displayCoordinate();});
canvas.addEventListener('click',event=>{
 if(!states)return;
 const rect=canvas.getBoundingClientRect();
 x=clamp(Math.floor((event.clientX-rect.left)*64/rect.width));
 y=clamp(Math.floor((event.clientY-rect.top)*64/rect.height));
 displayCoordinate();
});
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
const viewerPath=new URL('index.html',exampleUrl).href;
byId('open-viewer').href=viewerPath;
byId('start-viewer').addEventListener('click',()=>{
 const iframe=byId('original-viewer');
 iframe.src=viewerPath;
 iframe.hidden=false;
 byId('viewer-placeholder').hidden=true;
 iframe.focus();
});
