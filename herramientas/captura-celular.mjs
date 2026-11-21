// Captura la página completa en 390 px con escala 2x (780 px) e imprime la posición de las secciones (para el video).
// Uso: node herramientas/captura-celular.mjs <url> <salida.png> <carpeta-perfil>
import { spawn } from 'node:child_process'; import fs from 'node:fs';
const [url, out, prof] = process.argv.slice(2);
const ch = spawn('chromium', ['--headless=new','--disable-gpu','--hide-scrollbars','--remote-debugging-port=9333',`--user-data-dir=${prof}`,'about:blank'], {stdio:'ignore'});
const sleep = ms => new Promise(r=>setTimeout(r,ms));
let ws; for (let i=0;i<40;i++){ try{ const l = await (await fetch('http://127.0.0.1:9333/json')).json(); const p=l.find(x=>x.type==='page'); if(p){ws=new WebSocket(p.webSocketDebuggerUrl);break;} }catch{} await sleep(250); }
await new Promise(r=>ws.onopen=r); let id=0; const pend={};
ws.onmessage=e=>{const m=JSON.parse(e.data); if(m.id&&pend[m.id]){pend[m.id](m.result);delete pend[m.id];}};
const S=(method,params={})=>new Promise(r=>{const i=++id;pend[i]=r;ws.send(JSON.stringify({id:i,method,params}));});
await S('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:2,mobile:true});
await S('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
await S('Page.enable'); await S('Page.navigate',{url}); await sleep(3000);
await S('Runtime.evaluate',{expression:`(async()=>{for(let y=0;y<document.documentElement.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,120));}scrollTo(0,0);})()`,awaitPromise:true});
await sleep(1500);
const {result:sec}=await S('Runtime.evaluate',{expression:'JSON.stringify([...document.querySelectorAll("main > section")].map(s=>[s.id,Math.round(s.getBoundingClientRect().top+scrollY)]))',returnByValue:true});
await S('Runtime.evaluate',{expression:`document.querySelectorAll('body *').forEach(e=>{const h=e.getBoundingClientRect().height;if((e.tagName==='SECTION'||e.tagName==='HEADER')&&h>300){e.style.height=h+'px';e.style.minHeight=h+'px';}});document.querySelectorAll('*').forEach(e=>{if(getComputedStyle(e).position==='fixed')e.style.display='none'});`});
const {result} = await S('Runtime.evaluate',{expression:'document.documentElement.scrollHeight',returnByValue:true});
const {data}=await S('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:390,height:result.value,scale:1}});
fs.writeFileSync(out,Buffer.from(data,'base64')); console.log('ok',result.value,sec.value); ws.close(); ch.kill(); process.exit(0);
