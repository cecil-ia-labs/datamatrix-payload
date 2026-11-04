import {states} from "./state-data.js";

const words = {
  en: {
    pageTitle:"State viewer",title:"Choose a state.",intro:"Click the matrix to pause the sequence and copy its hexadecimal code.",
    cadence:"State cadence",minute:"One state per minute",second:"One state per second",fast:"Eight states per second",
    resume:"Resume",next:"Next state",code:"Selected hexadecimal code",note:"Public study sequence · Request for Discussion",
    running:"Running",paused:"Paused",state:"State",copied:"Paused. The hexadecimal code was copied.",
    manual:"Paused. Select the code below and copy it manually.",ready:"The sequence is in the app. Choose a state when you need it.",
    matrix:"Pause and copy the current state"
  },
  pt: {
    pageTitle:"Visualizador de estados",title:"Escolha um estado.",intro:"Clique na matriz para pausar a sequência e copiar seu código hexadecimal.",
    cadence:"Cadência dos estados",minute:"Um estado por minuto",second:"Um estado por segundo",fast:"Oito estados por segundo",
    resume:"Continuar",next:"Próximo estado",code:"Código hexadecimal selecionado",note:"Sequência pública de estudo · Request for Discussion",
    running:"Em execução",paused:"Pausado",state:"Estado",copied:"Pausado. O código hexadecimal foi copiado.",
    manual:"Pausado. Selecione o código abaixo e copie manualmente.",ready:"A sequência está no app. Escolha um estado quando precisar.",
    matrix:"Pausar e copiar o estado atual"
  }
};
let language="en", index=0, running=true, timer=null, statusKey="ready";
const byId=id=>document.getElementById(id);
function draw() {
  byId("state-image").src="data:image/gif;base64,"+states[index].gif_base64;
  byId("code").value=states[index].code_hex;
  byId("state-label").textContent=words[language].state+" "+(index+1)+" / "+states.length;
  byId("mode-label").textContent=words[language][running?"running":"paused"];
}
function schedule() {
  clearInterval(timer);
  if (running) timer=setInterval(()=>{index=(index+1)%states.length;draw();},Number(byId("period").value));
}
function translate() {
  document.documentElement.lang=language;
  document.title="Quad-Dimensional DataMatrix · "+words[language].pageTitle;
  document.querySelectorAll("[data-i18n]").forEach(node=>node.textContent=words[language][node.dataset.i18n]);
  byId("language").textContent=language==="en"?"Português":"English";
  byId("matrix").setAttribute("aria-label",words[language].matrix);
  byId("status").textContent=words[language][statusKey];
  draw();
}
async function choose() {
  running=false;schedule();draw();
  const selectedCode=states[index].code_hex;
  try {
    await navigator.clipboard.writeText(selectedCode);
    statusKey="copied";
  } catch {
    statusKey="manual";byId("code").focus();byId("code").select();
  }
  byId("status").textContent=words[language][statusKey];
}
byId("matrix").addEventListener("click",choose);
byId("resume").addEventListener("click",()=>{running=true;statusKey="ready";schedule();translate();});
byId("next").addEventListener("click",()=>{running=false;schedule();index=(index+1)%states.length;draw();});
byId("period").addEventListener("change",schedule);
byId("language").addEventListener("click",()=>{language=language==="en"?"pt":"en";translate();});
translate();schedule();
