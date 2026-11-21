// Verifica en celular (390x844) que el botón principal aparezca sin desplazar. Uso: BASE=http://127.0.0.1:8000/ node herramientas/verificar-boton.mjs <id...>
import { spawn } from 'node:child_process';
const ids = process.argv.slice(2), port = 9334;
const ch = spawn('chromium', ['--headless=new','--disable-gpu',`--remote-debugging-port=${port}`,`--user-data-dir=${(process.env.TMPDIR||'/tmp')+'/cdp-dobra'}`,'about:blank'],{stdio:'ignore'});
const sleep = ms => new Promise(r => setTimeout(r, ms));
for (let i=0;i<60;i++){try{await fetch(`http://127.0.0.1:${port}/json/version`);break}catch{await sleep(250)}}
const t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();
const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r=>ws.onopen=r);
let n=0; const p=new Map(); ws.onmessage=e=>{const m=JSON.parse(e.data); if(m.id&&p.has(m.id)){p.get(m.id)(m);p.delete(m.id)}};
const send=(method,params={})=>new Promise(r=>{const id=++n;p.set(id,r);ws.send(JSON.stringify({id,method,params}))});
const out=[];
try{
for (const [W,H] of [[390,844]]) for (const id of ids){
  await send('Emulation.setDeviceMetricsOverride',{width:W,height:H,deviceScaleFactor:1,mobile:W<600});
  await send('Page.navigate',{url:`${process.env.BASE||'http://127.0.0.1:8766/'}${id}/`}); await sleep(1400);
  const r=await send('Runtime.evaluate',{expression:"(async()=>{await document.fonts.ready;await new Promise(r=>setTimeout(r,1000));return document.querySelector('.hero .acoes .btn').getBoundingClientRect().bottom})()",awaitPromise:true,returnByValue:true});
  const b=r.result.result.value; if(b>H) out.push(`${W}x${H} ${id}: botón en ${Math.round(b)}`);
}} finally {ws.close(); ch.kill()}
console.log(out.join('\n')||'todo ok: el botón aparece sin desplazar');
