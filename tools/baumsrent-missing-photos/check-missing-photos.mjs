#!/usr/bin/env node
// Saskaita preces bez fotogrāfijas vietnē (noklusēti baumsrent.lv).
//
// Lietošana (vietējā datorā, kur nav egress bloka):
//   node check-missing-photos.mjs
//   node check-missing-photos.mjs --base https://baumsrent.lv --out result.csv
//   node check-missing-photos.mjs --browser        # ja katalogs ir JS-renderēts (vajag Playwright)
//   node check-missing-photos.mjs --product-re "/produkts/|/prece/"   # precizē produktu URL filtru
//
// Prasa tikai Node 18+ (iebūvēts fetch). Placeholder-attēli tiek skaitīti kā "nav foto".

import { writeFileSync } from 'node:fs';

// ---------- Argumenti ----------
const args = process.argv.slice(2);
function arg(name, def) {
  const i = args.indexOf(`--${name}`);
  if (i === -1) return def;
  const v = args[i + 1];
  return v && !v.startsWith('--') ? v : true;
}
const BASE = String(arg('base', 'https://baumsrent.lv')).replace(/\/+$/, '');
const OUT = String(arg('out', 'preces-bez-foto.csv'));
const USE_BROWSER = arg('browser', false) === true;
const CONCURRENCY = Number(arg('concurrency', 6));
const DELAY_MS = Number(arg('delay', 150));
const LIMIT = Number(arg('limit', 0)); // 0 = bez ierobežojuma (noderīgi testam)
const PRODUCT_RE = arg('product-re', null) ? new RegExp(String(arg('product-re')), 'i') : null;

const UA = 'Mozilla/5.0 (compatible; MissingPhotoAudit/1.0; +local-run)';

// Vārdi, kas norāda uz placeholder / "nav attēla" bildi -> skaitām kā bez foto.
const PLACEHOLDER_RE = /(placeholder|no[-_]?image|noimage|no[-_]?photo|nofoto|bez[-_]?foto|default[-_]?product|dummy|coming[-_]?soon|blank|spacer|1x1|missing)/i;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function get(url) {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml' }, redirect: 'follow' });
    if (!res.ok) return { ok: false, status: res.status, text: '' };
    return { ok: true, status: res.status, text: await res.text() };
  } catch (e) {
    return { ok: false, status: 0, text: '', error: e.message };
  }
}

// ---------- 1. Produktu URL atrašana caur sitemap ----------
function extractLocs(xml) {
  return [...xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/gi)].map((m) => m[1].trim());
}

async function fromSitemaps() {
  const seeds = [
    `${BASE}/sitemap.xml`,
    `${BASE}/sitemap_index.xml`,
    `${BASE}/sitemap-index.xml`,
    `${BASE}/product-sitemap.xml`,
    `${BASE}/wp-sitemap.xml`,
  ];
  const queue = [];
  const seen = new Set();
  for (const s of seeds) {
    const r = await get(s);
    if (r.ok && r.text.includes('<loc')) queue.push(...extractLocs(r.text));
  }
  const urls = new Set();
  // Dažas sitemap norādes ir uz citām sitemap; ejam vienu līmeni dziļāk.
  const nested = [];
  for (const u of queue) {
    if (/sitemap.*\.xml/i.test(u)) nested.push(u);
    else urls.add(u);
  }
  for (const n of nested) {
    if (seen.has(n)) continue;
    seen.add(n);
    const r = await get(n);
    if (r.ok) extractLocs(r.text).forEach((u) => { if (!/\.xml/i.test(u)) urls.add(u); });
  }
  return [...urls];
}

// ---------- 1b. Rezerves variants: vienkārša rāpošana no sākumlapas ----------
async function crawl() {
  const host = new URL(BASE).host;
  const seen = new Set([BASE + '/']);
  const found = new Set();
  let frontier = [BASE + '/'];
  const MAX_PAGES = 400;
  let visited = 0;
  while (frontier.length && visited < MAX_PAGES) {
    const batch = frontier.splice(0, CONCURRENCY);
    await Promise.all(batch.map(async (url) => {
      visited++;
      const r = await get(url);
      if (!r.ok) return;
      for (const m of r.text.matchAll(/href=["']([^"'#]+)["']/gi)) {
        let href = m[1];
        try { href = new URL(href, url).toString(); } catch { continue; }
        if (new URL(href).host !== host) continue;
        href = href.split('#')[0];
        if (/\.(jpg|jpeg|png|gif|svg|css|js|pdf|zip|webp)(\?|$)/i.test(href)) continue;
        found.add(href);
        if (!seen.has(href) && seen.size < MAX_PAGES * 3) { seen.add(href); frontier.push(href); }
      }
    }));
    await sleep(DELAY_MS);
  }
  return [...found];
}

// Heiristika: kuras lapas izskatās pēc produkta.
function looksLikeProduct(url) {
  if (PRODUCT_RE) return PRODUCT_RE.test(url);
  return /\/(produkts|produkti|prece|preces|product|products|item|shop|veikals|katalogs|noma|iznoma)\//i.test(url);
}

// ---------- 2. Attēla noteikšana produkta lapā ----------
function extractTitle(html) {
  const og = html.match(/<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)["']/i);
  if (og) return og[1].trim();
  const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1) return h1[1].replace(/<[^>]+>/g, '').trim();
  const t = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  return t ? t[1].trim() : '';
}

function hasRealPhoto(html) {
  // 1) og:image
  const ogs = [...html.matchAll(/<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["']/gi)].map((m) => m[1]);
  const realOg = ogs.filter((u) => u && !PLACEHOLDER_RE.test(u) && !/logo|favicon|icon/i.test(u));
  if (realOg.length) return { has: true, reason: 'og:image', sample: realOg[0] };

  // 2) Produktu galerijas / satura attēli (izlaižam logo, ikonas, placeholder)
  const imgs = [...html.matchAll(/<img[^>]+>/gi)].map((m) => m[0]);
  const candidates = [];
  for (const tag of imgs) {
    const src = (tag.match(/(?:data-src|data-large_image|srcset|src)=["']([^"']+)["']/i) || [])[1];
    if (!src) continue;
    if (/logo|favicon|icon|sprite|avatar|payment|badge|social/i.test(src)) continue;
    if (PLACEHOLDER_RE.test(src) || PLACEHOLDER_RE.test(tag)) continue;
    // Meklējam produkta/galerijas kontekstu, ja iespējams
    candidates.push(src);
  }
  // Vismaz viens "īsts" attēls satura zonā
  const galleryHint = /class=["'][^"']*(product|gallery|woocommerce-product|single-product|thumbnail|attachment)[^"']*["'][^>]*>[\s\S]{0,200}?<img/i.test(html);
  if (candidates.length && galleryHint) return { has: true, reason: 'gallery', sample: candidates[0] };
  if (candidates.length >= 1) return { has: true, reason: 'img', sample: candidates[0] };

  // 3) Ir tikai placeholder?
  const anyPlaceholder = imgs.some((t) => PLACEHOLDER_RE.test(t));
  return { has: false, reason: anyPlaceholder ? 'tikai-placeholder' : 'nav-attela', sample: '' };
}

// ---------- Browser (JS-renderēts) variants ----------
async function renderWithBrowser(urls) {
  let chromium;
  try { ({ chromium } = await import('playwright')); }
  catch { console.error('Playwright nav uzstādīts. Palaid: npm i -D playwright && npx playwright install chromium'); process.exit(1); }
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ userAgent: UA });
  const results = [];
  for (const url of urls) {
    const page = await ctx.newPage();
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      const html = await page.content();
      results.push({ url, title: extractTitle(html), ...hasRealPhoto(html) });
    } catch (e) {
      results.push({ url, title: '', has: false, reason: 'kluda:' + e.message.split('\n')[0], sample: '' });
    } finally { await page.close(); }
  }
  await browser.close();
  return results;
}

// ---------- Galvenā plūsma ----------
async function poolMap(items, fn) {
  const out = [];
  let i = 0;
  async function worker() {
    while (i < items.length) {
      const idx = i++;
      out[idx] = await fn(items[idx], idx);
      await sleep(DELAY_MS);
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  return out;
}

(async () => {
  console.log(`Bāze: ${BASE}`);
  console.log('Meklēju produktu lapas caur sitemap...');
  let all = await fromSitemaps();
  if (!all.length) {
    console.log('Sitemap nav / tukša — pāreju uz rāpošanu no sākumlapas...');
    all = await crawl();
  }
  let products = all.filter(looksLikeProduct);
  if (!products.length) {
    console.log('Heiristika neatrada produktu URL. Rādu pirmos 40 atrastos URL, lai vari norādīt --product-re:');
    all.slice(0, 40).forEach((u) => console.log('  ', u));
    console.log(`\nKopā atrasti ${all.length} URL. Palaid vēlreiz ar --product-re "tavs/regex".`);
    return;
  }
  products = [...new Set(products)];
  if (LIMIT) products = products.slice(0, LIMIT);
  console.log(`Atrastas ${products.length} produktu lapas. Pārbaudu attēlus${USE_BROWSER ? ' (browser)' : ''}...`);

  const results = USE_BROWSER
    ? await renderWithBrowser(products)
    : await poolMap(products, async (url) => {
        const r = await get(url);
        if (!r.ok) return { url, title: '', has: false, reason: 'nepieejama:' + r.status, sample: '' };
        return { url, title: extractTitle(r.text), ...hasRealPhoto(r.text) };
      });

  const missing = results.filter((r) => !r.has);
  console.log('\n================ REZULTĀTS ================');
  console.log(`Kopā produktu lapas: ${results.length}`);
  console.log(`Bez fotogrāfijas:    ${missing.length}`);
  console.log('===========================================\n');
  if (missing.length) {
    console.log('Preces bez foto:');
    missing.forEach((r, i) => console.log(`${String(i + 1).padStart(3)}. [${r.reason}] ${r.title || '(bez nosaukuma)'}\n     ${r.url}`));
  }

  const csv = ['nosaukums,url,iemesls', ...missing.map((r) =>
    `"${(r.title || '').replace(/"/g, '""')}","${r.url}","${r.reason}"`)].join('\n');
  writeFileSync(OUT, csv, 'utf8');
  console.log(`\nCSV saglabāts: ${OUT}`);
})();
