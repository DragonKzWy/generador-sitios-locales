// Capturas de página completa (computador 1440x900 y celular 390x844). Uso: BASE=http://127.0.0.1:8000/ node herramientas/capturas.mjs <id...>
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
const ids = process.argv.slice(2);
const port = 9333;
const ch = spawn('chromium', ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--remote-debugging-port=${port}`, `--user-data-dir=${(process.env.TMPDIR||'/tmp')+'/cdp-generador'}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
for (let i = 0; i < 60; i++) { try { await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); break; } catch { await sleep(250); } }
const tgt = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })).json();
const ws = new WebSocket(tgt.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let n = 0; const pend = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
const send = (method, params = {}) => new Promise(r => { const id = ++n; pend.set(id, r); ws.send(JSON.stringify({ id, method, params })); });
const ev = async js => (await send('Runtime.evaluate', { expression: js, awaitPromise: true, returnByValue: true })).result?.result?.value;
await send('Page.enable');
mkdirSync('capturas', { recursive: true });
try {
for (const id of ids) for (const [w, h, mob] of [[1440, 900, false], [390, 844, true]]) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: mob });
  await send('Page.navigate', { url: `${process.env.BASE||'http://127.0.0.1:8766/'}${id}/` });
  await sleep(2000);
  await ev(`(async()=>{document.documentElement.style.scrollBehavior='auto';for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,50))}scrollTo(0,0);
    document.querySelectorAll('.hero').forEach(x=>{const v=x.getBoundingClientRect().height+'px';x.style.minHeight=v;x.style.height=v});
    document.querySelectorAll('.hero .h-foto').forEach(x=>{x.style.height=x.getBoundingClientRect().height+'px'});
    document.querySelectorAll('.barra').forEach(x=>x.style.display='none');
    await document.fonts.ready; await new Promise(r=>setTimeout(r,400)); return 1})()`);
  const H = await ev('document.documentElement.scrollHeight');
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: H, deviceScaleFactor: 1, mobile: mob });
  await sleep(600);
  const r = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`capturas/${id}-${w}.png`, Buffer.from(r.result.data, 'base64'));
  console.log(`saved capturas/${id}-${w}.png ${w}x${H}`);
}
} finally { ws.close(); ch.kill(); }
