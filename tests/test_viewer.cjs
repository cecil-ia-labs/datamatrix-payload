/* Deterministic DOM-event checks for the app flow; Node.js, no dependencies. */
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const root=path.resolve(__dirname,"..");
class Element {
  constructor(){this.listeners={};this.textContent="";this.value="";this.attrs={};this.dataset={};}
  addEventListener(type,handler){this.listeners[type]=handler;}
  setAttribute(name,value){this.attrs[name]=value;}
  focus(){this.focused=true;}
  select(){this.selectionStart=0;this.selectionEnd=this.value.length;}
  async fire(type){if(this.listeners[type])await this.listeners[type]();}
}
(async()=>{
  const ids=["state-image","code","state-label","mode-label","period","status","language","matrix","resume","next"];
  const elements=Object.fromEntries(ids.map(id=>[id,new Element()]));
  elements.period.value="60000";
  const html=fs.readFileSync(path.join(root,"examples/index.html"),"utf8");
  for(const id of ids)assert.ok(html.includes('id="'+id+'"'),"Missing HTML element "+id);
  const translated=[...html.matchAll(/data-i18n="([^"]+)"/g)].map(match=>{
    const node=new Element();node.dataset.i18n=match[1];return node;
  });
  let now=0,identifier=0,copied=null;
  const timers=new Map();
  const document={documentElement:{lang:"en"},title:"",
    getElementById:id=>elements[id],querySelectorAll:()=>translated};
  const navigator={clipboard:{writeText:async text=>{copied=text;}}};
  const context=vm.createContext({document,navigator,console,
    setInterval:(callback,delay)=>{timers.set(++identifier,{callback,delay,next:now+delay});return identifier;},
    clearInterval:id=>timers.delete(id)});
  const data=fs.readFileSync(path.join(root,"examples/state-data.js"),"utf8").replace("export const states","const states");
  const source=fs.readFileSync(path.join(root,"examples/viewer.js"),"utf8").replace(/^import .*;\s*/,"");
  vm.runInContext(data+"\n"+source,context);
  function advance(milliseconds){
    const end=now+milliseconds;
    while(true){
      const pending=[...timers.entries()].filter(([,t])=>t.next<=end).sort((a,b)=>a[1].next-b[1].next)[0];
      if(!pending)break;
      const [id,timer]=pending;now=timer.next;timer.next+=timer.delay;timer.callback();
    }
    now=end;
  }
  assert.equal(document.documentElement.lang,"en");
  assert.equal(elements["state-label"].textContent,"State 1 / 16");
  assert.equal([...timers.values()][0].delay,60000);
  advance(59999);
  assert.equal(elements["state-label"].textContent,"State 1 / 16");
  advance(1);
  assert.equal(elements["state-label"].textContent,"State 2 / 16");
  const expected=elements.code.value;
  assert.match(expected,/^[0-9A-F]{6144}$/);
  await elements.matrix.fire("click");
  assert.equal(copied,expected);
  assert.equal(timers.size,0);
  const frozen=elements["state-image"].src;
  advance(120000);
  assert.equal(elements["state-image"].src,frozen);
  assert.equal(elements["mode-label"].textContent,"Paused");
  await elements.language.fire("click");
  assert.equal(document.documentElement.lang,"pt");
  assert.equal(document.title,"Quad-Dimensional DataMatrix · Visualizador de estados");
  assert.equal(elements["mode-label"].textContent,"Pausado");
  assert.ok(translated.every(node=>node.textContent));
  await elements.language.fire("click");
  elements.period.value="125";
  await elements.period.fire("change");
  await elements.resume.fire("click");
  advance(125);
  assert.equal(elements["state-label"].textContent,"State 3 / 16");
  navigator.clipboard.writeText=async()=>{throw new Error("Clipboard unavailable");};
  await elements.matrix.fire("click");
  assert.equal(timers.size,0);
  assert.ok(elements.status.textContent.includes("manually"));
  assert.equal(elements.code.selectionEnd-elements.code.selectionStart,6144);
  console.log("Viewer DOM checks passed: cadence, pause, exact copy, language, resume, manual copy.");
})().catch(error=>{console.error(error);process.exitCode=1;});
