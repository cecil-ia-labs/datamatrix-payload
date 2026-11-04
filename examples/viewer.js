import {states} from "./state-data.js";

const words = {
  en: {
    pageTitle:"State viewer",title:"Choose a state.",intro:"Pause the matrix, copy a color, and try it on the receiving side.",
    selectStep:"01 · Select",receiveStep:"02 · Receive",receiveTitle:"Paste the color.",receiveIntro:"Click or tap the circle to read the copied code.",
    cadence:"State cadence",minute:"One state per minute",second:"One state per second",fast:"Eight states per second",
    resume:"Resume",next:"Next state",note:"Public study sequence · Request for Discussion",
    running:"Running",paused:"Paused",state:"State",copied:"Paused. Six-character color copied.",
    manual:"Paused. Copy the six-character code below.",manualCode:"Copy this code",ready:"Click the matrix to choose its current state.",
    matrix:"Pause and copy a six-character color",codeSource:"Code source",module:"Selected module",first:"First module · (0, 0)",last:"Last module · (63, 63)",coordinates:"Choose coordinates",
    invalidCoordinates:"Choose whole-number coordinates between 0 and 63.",paste:"Paste the copied color",pasteReady:"Your selected color will appear here.",
    pasteSuccess:"Color received successfully.",pasteManual:"Paste into the field below, or enter the code.",pasteCode:"Paste or enter six hexadecimal characters",
    pasteInvalid:"Use exactly six hexadecimal characters.",pasteMismatch:"This color does not match your selected code.",pasteFirst:"Choose a state on the matrix first.",
    clipboard:"Clipboard",cleanupIdle:"Attempts to clear the copied code after 30 seconds.",cleanupWaiting:"Cleanup is scheduled for 30 seconds after copying.",
    cleanupCleared:"The copied code was cleared from the clipboard.",cleanupChanged:"The clipboard changed. Its new contents were kept.",
    cleanupBlocked:"Automatic cleanup was unavailable. You can clear the copied code below.",cleanupFocus:"Cleanup will be attempted when you return to this tab.",clearNow:"Clear copied code"
  },
  pt: {
    pageTitle:"Visualizador de estados",title:"Escolha um estado.",intro:"Pause a matriz, copie uma cor e experimente no lado receptor.",
    selectStep:"01 · Selecione",receiveStep:"02 · Receba",receiveTitle:"Cole a cor.",receiveIntro:"Clique ou toque no círculo para ler o código copiado.",
    cadence:"Cadência dos estados",minute:"Um estado por minuto",second:"Um estado por segundo",fast:"Oito estados por segundo",
    resume:"Continuar",next:"Próximo estado",note:"Sequência pública de estudo · Request for Discussion",
    running:"Em execução",paused:"Pausado",state:"Estado",copied:"Pausado. Cor de seis caracteres copiada.",
    manual:"Pausado. Copie o código de seis caracteres abaixo.",manualCode:"Copie este código",ready:"Clique na matriz para escolher o estado atual.",
    matrix:"Pausar e copiar uma cor de seis caracteres",codeSource:"Origem do código",module:"Módulo selecionado",first:"Primeiro módulo · (0, 0)",last:"Último módulo · (63, 63)",coordinates:"Escolher coordenadas",
    invalidCoordinates:"Escolha coordenadas inteiras entre 0 e 63.",paste:"Colar a cor copiada",pasteReady:"Sua cor selecionada aparecerá aqui.",
    pasteSuccess:"Cor recebida com sucesso.",pasteManual:"Cole no campo abaixo ou digite o código.",pasteCode:"Cole ou digite seis caracteres hexadecimais",
    pasteInvalid:"Use exatamente seis caracteres hexadecimais.",pasteMismatch:"Esta cor não corresponde ao código selecionado.",pasteFirst:"Escolha um estado na matriz primeiro.",
    clipboard:"Área de transferência",cleanupIdle:"Tenta limpar o código copiado após 30 segundos.",cleanupWaiting:"Limpeza agendada para 30 segundos após a cópia.",
    cleanupCleared:"O código copiado foi limpo da área de transferência.",cleanupChanged:"A área de transferência mudou. O novo conteúdo foi mantido.",
    cleanupBlocked:"A limpeza automática não foi possível. Você pode limpar o código abaixo.",cleanupFocus:"A limpeza será tentada quando você voltar a esta aba.",clearNow:"Limpar código copiado"
  }
};
const HIGHLIGHT_MS=2500, CLIPBOARD_MS=30000;
const byId=id=>document.getElementById(id);
let language="en", index=0, running=true, timer=null, highlightTimer=null;
let statusKey="ready", pasteKey="pasteReady", clipboardKey="cleanupIdle";
let selection=null, lease=null, cleanupTimer=null, operation=0, clipboardBusy=false;

function renderMessages() {
  byId("status").textContent=words[language][statusKey];
  byId("paste-status").textContent=words[language][pasteKey];
  byId("paste-status").dataset.kind=pasteKey==="pasteSuccess"?"success":
    ["pasteInvalid","pasteMismatch"].includes(pasteKey)?"error":"";
  byId("clipboard-status").textContent=words[language][clipboardKey];
  byId("clear-clipboard").hidden=!lease || !["cleanupBlocked","cleanupFocus"].includes(clipboardKey);
}
function position() {
  if(byId("source").value==="last") return {x:63,y:63};
  if(byId("source").value!=="coordinates") return {x:0,y:0};
  const x=Number(byId("source-x").value), y=Number(byId("source-y").value);
  if(byId("source-x").value==="" || byId("source-y").value==="" ||
    ![x,y].every(n=>Number.isInteger(n)&&n>=0&&n<64)) return null;
  return {x,y};
}
function colorAt(state,{x,y}) {
  const offset=2*(y*64+x);
  const dimension=Number.parseInt(state.module_indices_hex.slice(offset,offset+2),16);
  return state.palette_hex[dimension].slice(1).toUpperCase();
}
function draw() {
  byId("state-image").src="data:image/gif;base64,"+states[index].gif_base64;
  byId("state-label").textContent=words[language].state+" "+(index+1)+" / "+states.length;
  byId("mode-label").textContent=words[language][running?"running":"paused"];
}
function schedule() {
  clearInterval(timer);
  if(running) timer=setInterval(()=>{index=(index+1)%states.length;draw();},Number(byId("period").value));
}
function clearHighlight() {
  clearTimeout(highlightTimer);
  byId("matrix-frame").classList.remove("highlight");
}
function highlight(code) {
  clearHighlight();
  byId("matrix-frame").style.setProperty("--selected-color","#"+code);
  byId("matrix-frame").classList.add("highlight");
  highlightTimer=setTimeout(clearHighlight,HIGHLIGHT_MS);
}
function resetReceiver() {
  byId("paste-target").classList.remove("received");
  byId("target-symbol").textContent="↘";
  byId("received-code").textContent="—";
  byId("paste-code").value="";
  byId("manual-paste").hidden=true;
  pasteKey="pasteReady";
}
function hasFocus() {
  return document.visibilityState==="visible" && document.hasFocus();
}
function forgetLease(current,key) {
  if(lease!==current) return;
  clearTimeout(cleanupTimer);
  lease=null;clipboardKey=key;renderMessages();
}
async function clearCopiedCode(userGesture=false) {
  const current=lease;
  if(!current || clipboardBusy) return;
  if(!hasFocus()) {clipboardKey="cleanupFocus";renderMessages();return;}
  clipboardBusy=true;
  try {
    // Background reads must not request permission or guess what is on the clipboard.
    if(!userGesture) {
      const permission=await navigator.permissions?.query({name:"clipboard-read"});
      if(permission?.state!=="granted") throw new Error("Clipboard read is not granted");
    }
    const text=await navigator.clipboard.readText();
    if(lease!==current) return;
    if(text!==current.code) {forgetLease(current,"cleanupChanged");return;}
    if(!hasFocus()) {clipboardKey="cleanupFocus";renderMessages();return;}
    await navigator.clipboard.writeText("");
    forgetLease(current,"cleanupCleared");
  } catch {
    if(lease===current) {clipboardKey="cleanupBlocked";renderMessages();}
  } finally {clipboardBusy=false;}
}
function armCleanup(code) {
  clearTimeout(cleanupTimer);
  lease={code,deadline:Date.now()+CLIPBOARD_MS};
  clipboardKey="cleanupWaiting";
  cleanupTimer=setTimeout(()=>clearCopiedCode(),CLIPBOARD_MS);
  renderMessages();
}
function translate() {
  document.documentElement.lang=language;
  document.title="Quad-Dimensional DataMatrix · "+words[language].pageTitle;
  document.querySelectorAll("[data-i18n]").forEach(node=>node.textContent=words[language][node.dataset.i18n]);
  byId("language").textContent=language==="en"?"Português":"English";
  byId("matrix").setAttribute("aria-label",words[language].matrix);
  byId("paste-target").setAttribute("aria-label",words[language].paste);
  draw();renderMessages();
}
async function choose() {
  if(clipboardBusy) return;
  const coordinates=position();
  if(!coordinates) {statusKey="invalidCoordinates";renderMessages();return;}
  const request=++operation;
  running=false;schedule();draw();
  const code=colorAt(states[index],coordinates);
  selection={code,index,...coordinates};
  byId("code").value=code;byId("manual-copy").hidden=true;
  resetReceiver();highlight(code);
  clipboardBusy=true;
  try {
    await navigator.clipboard.writeText(code);
    if(request!==operation) return;
    statusKey="copied";armCleanup(code);
  } catch {
    if(request!==operation) return;
    statusKey="manual";byId("manual-copy").hidden=false;
    byId("code").focus();byId("code").select();
  } finally {clipboardBusy=false;renderMessages();retryCleanup();}
}
function receive(text) {
  byId("paste-target").classList.remove("received");
  byId("target-symbol").textContent="↘";
  byId("received-code").textContent="—";
  const match=/^#?([0-9a-f]{6})$/i.exec(text.trim());
  if(!match) {pasteKey="pasteInvalid";renderMessages();return;}
  if(!selection) {pasteKey="pasteFirst";renderMessages();return;}
  const code=match[1].toUpperCase();
  if(code!==selection.code) {pasteKey="pasteMismatch";renderMessages();return;}
  byId("paste-target").style.setProperty("--received-color","#"+code);
  byId("paste-target").classList.add("received");
  byId("target-symbol").textContent="✓";
  byId("received-code").textContent=code;
  byId("paste-code").value=code;byId("manual-paste").hidden=true;
  pasteKey="pasteSuccess";renderMessages();
}
async function paste() {
  if(!selection) {pasteKey="pasteFirst";renderMessages();return;}
  try {receive(await navigator.clipboard.readText());}
  catch {
    pasteKey="pasteManual";byId("manual-paste").hidden=false;
    byId("paste-code").focus();renderMessages();
  }
}
byId("matrix").addEventListener("click",choose);
byId("paste-target").addEventListener("click",paste);
byId("paste-code").addEventListener("paste",event=>{
  event.preventDefault();receive(event.clipboardData.getData("text/plain"));
});
byId("paste-code").addEventListener("input",()=>{
  if(byId("paste-code").value.trim().length>=6) receive(byId("paste-code").value);
});
byId("code").addEventListener("copy",event=>{
  if(!selection || !event.clipboardData) return;
  event.preventDefault();event.clipboardData.setData("text/plain",selection.code);
  statusKey="copied";armCleanup(selection.code);
});
byId("clear-clipboard").addEventListener("click",()=>clearCopiedCode(true));
byId("resume").addEventListener("click",()=>{if(clipboardBusy)return;running=true;clearHighlight();statusKey="ready";schedule();translate();});
byId("next").addEventListener("click",()=>{if(clipboardBusy)return;running=false;clearHighlight();schedule();index=(index+1)%states.length;draw();});
byId("period").addEventListener("change",schedule);
byId("source").addEventListener("change",()=>{byId("coordinates").hidden=byId("source").value!=="coordinates";});
byId("language").addEventListener("click",()=>{language=language==="en"?"pt":"en";translate();});
function retryCleanup() {if(lease && Date.now()>=lease.deadline) clearCopiedCode();}
document.addEventListener("visibilitychange",retryCleanup);
window.addEventListener("focus",retryCleanup);
translate();schedule();
