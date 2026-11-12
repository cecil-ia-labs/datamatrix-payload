/*
 * SPDX-FileCopyrightText: 2026 Cecil-IA Labs
 * SPDX-License-Identifier: MIT
 *
 * Author: João Paulo De Luca Jr.; Jorge Luiz Espanhol
 * Organization: Cecil-IA Labs
 * Project: Quad-Dimensional DataMatrix
 *
 * AI-assisted development:
 * OpenAI ChatGPT and Codex were used as development tools.
 * Human-directed development and integration.
 * No OpenAI sponsorship, affiliation, or endorsement is implied.
 *
 * License: See the repository LICENSE file and SPDX identifier above.
 */

/* Event and timer checks for the concept app; Node.js, no dependencies. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const root=path.resolve(__dirname,"..");
const html=fs.readFileSync(path.join(root,"examples/index.html"),"utf8");
const data=fs.readFileSync(path.join(root,"examples/state-data.js"),"utf8");
const states=JSON.parse(data.slice(data.indexOf("["),data.lastIndexOf("]")+1));
const source=fs.readFileSync(path.join(root,"examples/viewer.js"),"utf8").replace(/^import .*;\s*/,"");

class Element {
  constructor(){
    this.listeners={};this.textContent="";this.value="";this.attrs={};this.dataset={};this.hidden=false;
    this.classes=new Set();
    this.classList={add:name=>this.classes.add(name),remove:name=>this.classes.delete(name),contains:name=>this.classes.has(name)};
    this.style={values:{},setProperty:(name,value)=>{this.style.values[name]=value;}};
  }
  addEventListener(type,handler){(this.listeners[type]??=[]).push(handler);}
  setAttribute(name,value){this.attrs[name]=value;}
  focus(){this.focused=true;}
  select(){this.selectionStart=0;this.selectionEnd=this.value.length;}
  async fire(type,event={}){for(const handler of this.listeners[type]??[])await handler(event);}
}
function viewer(){
  const ids=[...html.matchAll(/id="([^"]+)"/g)].map(match=>match[1]);
  const elements=Object.fromEntries(ids.map(id=>[id,new Element()]));
  for(const id of ["manual-copy","manual-paste","clear-clipboard","coordinates"])elements[id].hidden=true;
  elements.period.value="60000";elements.source.value="first";
  elements["source-x"].value="0";elements["source-y"].value="0";
  const translated=[...html.matchAll(/data-i18n="([^"]+)"/g)].map(match=>{
    const node=new Element();node.dataset.i18n=match[1];return node;
  });
  let now=0,identifier=0;
  const timers=new Map();
  const h={elements,translated,text:null,writes:[],reads:0,permission:"granted",focused:true,readAllowed:true,writeAllowed:true};
  const document=new Element();
  Object.assign(document,{documentElement:{lang:"en"},title:"",visibilityState:"visible",hasFocus:()=>h.focused,
    getElementById:id=>elements[id],querySelectorAll:()=>translated});
  const window=new Element();
  const navigator={permissions:{query:async()=>({state:h.permission})},clipboard:{
    writeText:async text=>{if(!h.writeAllowed)throw Error("Write denied");h.text=text;h.writes.push(text);},
    readText:async()=>{h.reads++;if(!h.readAllowed)throw Error("Read denied");return h.text??"";}
  }};
  const addTimer=(callback,delay,repeat)=>{timers.set(++identifier,{callback,delay,next:now+delay,repeat});return identifier;};
  const context=vm.createContext({document,window,navigator,console,
    Date:class extends Date{static now(){return now;}},
    setInterval:(callback,delay)=>addTimer(callback,delay,true),clearInterval:id=>timers.delete(id),
    setTimeout:(callback,delay)=>addTimer(callback,delay,false),clearTimeout:id=>timers.delete(id)});
  vm.runInContext(data.replace("export const states","const states")+"\n"+source,context);
  h.document=document;h.window=window;
  h.click=id=>elements[id].fire("click");
  h.advance=async milliseconds=>{
    const end=now+milliseconds;
    while(true){
      const pending=[...timers.entries()].filter(([,t])=>t.next<=end).sort((a,b)=>a[1].next-b[1].next)[0];
      if(!pending)break;
      const [id,timer]=pending;now=timer.next;
      if(timer.repeat)timer.next+=timer.delay;else timers.delete(id);
      await timer.callback();
    }
    now=end;
  };
  return h;
}
function expected(state,x,y){
  const dimension=parseInt(states[state].module_indices_hex.slice(2*(y*64+x),2*(y*64+x)+2),16);
  return states[state].palette_hex[dimension].slice(1);
}
(async()=>{
  assert.equal(states.length,16);
  for(const state of states){
    assert.match(state.code_hex,/^[0-9A-F]{6}$/);
    assert.equal(state.module_indices_hex.length,8192);
    assert.equal(state.palette_hex.length,64);
  }
  let checks=0;
  async function check(name,run){await run();checks++;console.log("PASS: "+name);}
  await check("cadence, pause, six-character copy, and a 2.5-second highlight",async()=>{
    const h=viewer(),e=h.elements;
    await h.advance(59999);assert.equal(e["state-label"].textContent,"State 1 / 16");
    await h.advance(1);assert.equal(e["state-label"].textContent,"State 2 / 16");
    await h.click("matrix");
    assert.equal(h.text,expected(1,0,0));assert.equal(h.text.length,6);
    assert.equal(e["matrix-frame"].style.values["--selected-color"],"#"+h.text);
    assert.ok(e["matrix-frame"].classList.contains("highlight"));
    await h.advance(2499);assert.ok(e["matrix-frame"].classList.contains("highlight"));
    await h.advance(1);assert.ok(!e["matrix-frame"].classList.contains("highlight"));
    await h.advance(27500);assert.equal(h.text,"");
    assert.ok(e["clipboard-status"].textContent.includes("cleared"));
    await h.advance(90000);assert.equal(e["state-label"].textContent,"State 2 / 16");
  });
  await check("first, last, and explicit coordinates select palette colors",async()=>{
    const h=viewer(),e=h.elements;
    e.source.value="last";await h.click("matrix");assert.equal(h.text,expected(0,63,63));
    e.source.value="coordinates";await e.source.fire("change");assert.equal(e.coordinates.hidden,false);
    e["source-x"].value="17";e["source-y"].value="29";await h.click("matrix");
    assert.equal(h.text,expected(0,17,29));
    e["source-x"].value="64";const before=h.writes.length;await h.click("matrix");
    assert.equal(h.writes.length,before);assert.ok(e.status.textContent.includes("0 and 63"));
    e["source-x"].value="";await h.click("matrix");assert.equal(h.writes.length,before);
  });
  await check("one-click reception and normalization of a manually pasted color",async()=>{
    const h=viewer(),e=h.elements;
    await h.click("paste-target");assert.equal(h.reads,0);assert.ok(e["paste-status"].textContent.includes("first"));
    await h.click("matrix");await h.click("paste-target");
    assert.equal(e["received-code"].textContent,h.text);
    assert.equal(e["paste-target"].style.values["--received-color"],"#"+h.text);
    assert.ok(e["paste-status"].textContent.includes("successfully"));
    h.readAllowed=false;await h.click("paste-target");assert.equal(e["manual-paste"].hidden,false);
    await e["paste-code"].fire("paste",{preventDefault(){},clipboardData:{getData:()=>" #"+h.text.toLowerCase()+" "}});
    assert.equal(e["manual-paste"].hidden,true);
    assert.equal(e["paste-status"].dataset.kind,"success");
  });
  await check("invalid and mismatching pasted values never show success",async()=>{
    const h=viewer(),e=h.elements;await h.click("matrix");const code=h.text;
    h.text="not a code";await h.click("paste-target");
    assert.equal(e["paste-status"].dataset.kind,"error");
    h.text=code==="FFFFFF"?"000000":"FFFFFF";await h.click("paste-target");
    assert.ok(e["paste-status"].textContent.includes("does not match"));
    assert.equal(e["paste-target"].classList.contains("received"),false);
  });
  await check("new clipboard contents are preserved at the cleanup deadline",async()=>{
    const h=viewer();await h.click("matrix");h.text="another application's copied content";
    await h.advance(30000);
    assert.equal(h.text,"another application's copied content");assert.equal(h.writes.length,1);
    assert.ok(h.elements["clipboard-status"].textContent.includes("new contents"));
  });
  await check("background cleanup never prompts for clipboard permission",async()=>{
    const h=viewer();h.permission="prompt";await h.click("matrix");await h.advance(30000);
    assert.equal(h.reads,0);assert.equal(h.writes.length,1);
    assert.equal(h.elements["clear-clipboard"].hidden,false);
    await h.click("clear-clipboard");assert.equal(h.text,"");
  });
  await check("denied clipboard reads preserve the clipboard and offer manual cleanup",async()=>{
    const h=viewer();h.readAllowed=false;await h.click("matrix");const code=h.text;
    await h.advance(30000);assert.equal(h.text,code);
    assert.ok(h.elements["clipboard-status"].textContent.includes("unavailable"));
    await h.click("clear-clipboard");assert.equal(h.text,code);
  });
  await check("cleanup waits for focus and checks contents again on return",async()=>{
    const h=viewer();await h.click("matrix");h.focused=false;h.document.visibilityState="hidden";
    await h.advance(30000);assert.equal(h.reads,0);
    h.text="copied while away";h.focused=true;h.document.visibilityState="visible";
    await h.document.fire("visibilitychange");
    assert.equal(h.text,"copied while away");assert.equal(h.writes.length,1);
  });
  await check("a new copy restarts its own 30-second cleanup timer",async()=>{
    const h=viewer();await h.click("matrix");await h.advance(20000);
    await h.click("next");await h.click("matrix");const second=h.text;
    await h.advance(10000);assert.equal(h.text,second);assert.equal(h.writes.length,2);
    await h.advance(19999);assert.equal(h.text,second);
    await h.advance(1);assert.equal(h.text,"");assert.equal(h.writes.length,3);
  });
  await check("manual copy fallback exposes only six characters and arms cleanup on copying",async()=>{
    const h=viewer(),e=h.elements;h.writeAllowed=false;await h.click("matrix");
    assert.equal(e["manual-copy"].hidden,false);assert.match(e.code.value,/^[0-9A-F]{6}$/);
    assert.equal(e.code.selectionEnd-e.code.selectionStart,6);
    let copied;await e.code.fire("copy",{preventDefault(){},clipboardData:{setData:(_,value)=>{copied=value;h.text=value;}}});
    assert.equal(copied,e.code.value);h.writeAllowed=true;
    await h.advance(30000);assert.equal(h.text,"");
  });
  await check("language, resume, and fast cadence remain available",async()=>{
    const h=viewer(),e=h.elements;await h.click("matrix");await h.click("language");
    assert.equal(h.document.documentElement.lang,"pt");
    assert.equal(e["mode-label"].textContent,"Pausado");assert.ok(h.translated.every(n=>n.textContent));
    await h.click("paste-target");assert.ok(e["paste-status"].textContent.includes("sucesso"));
    e.period.value="125";await e.period.fire("change");await h.click("resume");await h.advance(125);
    assert.equal(e["state-label"].textContent,"Estado 2 / 16");
  });
  console.log("Viewer checks passed: "+checks+" scenarios.");
})().catch(error=>{console.error(error);process.exitCode=1;});
