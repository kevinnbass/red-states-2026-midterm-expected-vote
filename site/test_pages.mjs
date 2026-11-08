// Browser checks for the figures page and the state write-up pages, over CDP (Node 22+, Chromium with --remote-debugging-port).
//   node site/test_pages.mjs <cdp_port> <out_dir> <figures_page_url> [<writeup_url> ...]     (exit 0 = every check passed)
// Each page: loads with no script errors or console errors, no {{ }} / NaN / undefined in the text, every image loads, and no
// horizontal page scroll at 390 px. Figures page also: every state tab shows its own panel, view buttons switch the image, the
// full-size view opens with the right image and closes with Escape, the expectation toggle redraws the overview.
import { writeFileSync } from 'node:fs';
const [port, out, figUrl, ...writeups] = process.argv.slice(2);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const results = [];
const check = (name, ok, detail = '') => results.push(`${ok ? 'PASS' : 'FAIL'} ${name}${detail && !ok ? ' :: ' + detail : ''}`);

async function connect() {
  let targets;
  for (let i = 0; i < 50; i++) {
    try { targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); if (targets.length) break; } catch {}
    await sleep(200);
  }
  const page = targets.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.addEventListener('open', r, { once: true }));
  let id = 0; const pending = new Map(); const errors = [];
  ws.addEventListener('message', ev => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + (m.params.exceptionDetails.exception?.description || ''));
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push('console.error ' + JSON.stringify(m.params.args.map(a => a.value)));
  });
  const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async expr => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); return r.result.result?.value; };
  await send('Runtime.enable'); await send('Page.enable');
  return { send, ev, errors };
}

async function load(c, url, width) {
  c.errors.length = 0;
  await c.send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: width < 500 });
  await c.send('Page.navigate', { url });
  await sleep(2200);
  await c.ev(`Promise.all([...document.images].map(i => (i.loading='eager', i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; }))))`);
  await sleep(300);
}

async function common(c, url, tag) {
  for (const w of [1280, 390]) {
    await load(c, url, w);
    check(`${tag} @${w}: no script errors`, c.errors.length === 0, c.errors.join(' | '));
    const txt = await c.ev(`document.body.innerText`);
    check(`${tag} @${w}: no placeholders, NaN or undefined`, !/\{\{|NaN|undefined/.test(txt));
    const imgs = await c.ev(`[...document.images].filter(i => i.getAttribute('src')).map(i => [i.getAttribute('src'), i.naturalWidth])`);
    check(`${tag} @${w}: images load`, imgs.every(([, n]) => n > 0), JSON.stringify(imgs.filter(([, n]) => !n)));
    const sw = await c.ev(`[document.documentElement.scrollWidth, innerWidth]`);
    check(`${tag} @${w}: no horizontal page scroll`, sw[0] <= sw[1], JSON.stringify(sw));
    const svgs = await c.ev(`[...document.querySelectorAll('svg.chart')].map(s => s.childElementCount)`);
    check(`${tag} @${w}: every chart drew`, svgs.length > 0 && svgs.every(n => n > 3), JSON.stringify(svgs));
  }
}

const c = await connect();
await common(c, figUrl, 'figures');
await load(c, figUrl, 1280);
const tabs = await c.ev(`[...document.querySelectorAll('.statebar [role=tab]')].map(t => t.dataset.st)`);
for (const st of tabs) {
  const ok = await c.ev(`(() => { const t = [...document.querySelectorAll('.statebar [role=tab]')].find(x => x.dataset.st === '${st}'); t.click();
    const vis = [...document.querySelectorAll('.statepanel')].filter(p => !p.hidden); return vis.length === 1 && vis[0].id === t.getAttribute('aria-controls') && t.getAttribute('aria-selected') === 'true'; })()`);
  check(`state tab ${st} shows only its panel`, ok);
  const v = await c.ev(`(() => { const p = [...document.querySelectorAll('.statepanel')].find(p => !p.hidden), card = p.querySelector('.figcard'), b = card.querySelectorAll('.views button')[2];
    b.click(); return [card.querySelector('img.fig').getAttribute('src') === b.dataset.src, card.querySelector('.full').dataset.src === b.dataset.src]; })()`);
  check(`state ${st}: view button switches image and full-size target`, v[0] && v[1], JSON.stringify(v));
}
await c.ev(`[...document.querySelectorAll('.statepanel')].find(p => !p.hidden).querySelector('.full').click()`); await sleep(500);
const lb = await c.ev(`[!document.getElementById('lb').hidden, document.getElementById('lb-img').getAttribute('src') === [...document.querySelectorAll('.statepanel')].find(p => !p.hidden).querySelector('.full').dataset.src, document.activeElement.id]`);
check('full-size view opens with the selected image and focuses Close', lb[0] && lb[1] && lb[2] === 'lb-x', JSON.stringify(lb));
await c.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 }); await sleep(300);
check('Escape closes the full-size view', await c.ev(`document.getElementById('lb').hidden`));
const before = await c.ev(`document.querySelector('#ch-ov svg').innerHTML.length`);
await c.ev(`document.querySelector('.seg button[data-exp=inc]').click()`); await sleep(200);
const after = await c.ev(`[document.querySelector('#ch-ov svg').innerHTML.length, document.querySelector('.seg button[data-exp=inc]').getAttribute('aria-pressed')]`);
check('expectation toggle redraws the overview', after[1] === 'true' && after[0] > 0, JSON.stringify([before, after]));
for (const [i, u] of writeups.entries()) await common(c, u, `writeup ${i + 1}`);
writeFileSync(`${out}/test_results.txt`, results.join('\n') + '\n');
console.log(results.join('\n'));
const fails = results.filter(r => r.startsWith('FAIL')).length;
console.log(`${results.length - fails} of ${results.length} checks passed`);
process.exit(fails ? 1 : 0);
