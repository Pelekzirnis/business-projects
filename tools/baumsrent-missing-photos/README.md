# Preces bez fotogrāfijas — audita skripts

Saskaita, kurām precēm vietnē (noklusēti **baumsrent.lv**) nav fotogrāfijas.
Placeholder / "nav attēla" bildes tiek skaitītas kā **bez foto**.

> ⚠️ Palaidiet **lokāli uz sava datora** (attālinātajā Claude Code vidē `baumsrent.lv`
> ir bloķēts tīkla politikas dēļ). Prasa tikai **Node 18+** (iebūvēts `fetch`).

## Palaišana

```bash
cd tools/baumsrent-missing-photos
node check-missing-photos.mjs
```

Izvade: konsolē kopskaits + saraksts, un fails `preces-bez-foto.csv`.

## Ja katalogs ir JS-renderēts (SPA)

Ja skripts atrod maz/nulle produktu vai visi rāda "nav-attela", lapa, iespējams,
renderējas ar JavaScript. Tad:

```bash
npm i -D playwright && npx playwright install chromium
node check-missing-photos.mjs --browser
```

## Noderīgi karogi

| Karogs | Nozīme |
|--------|--------|
| `--base https://baumsrent.lv` | Cita vietne |
| `--product-re "/produkts/\|/prece/"` | Precizē, kuras lapas ir produkti (regex) |
| `--limit 20` | Testam — pārbauda tikai pirmās 20 preces |
| `--out fails.csv` | Cits CSV izvades ceļš |
| `--browser` | Lietot Playwright (JS lapām) |
| `--concurrency 6` `--delay 150` | Ātrums / saudzīgums pret serveri |

## Kā tas strādā

1. **Produktu URL:** vispirms no `sitemap.xml` / `wp-sitemap.xml` / `product-sitemap.xml`;
   ja nav — rāpo no sākumlapas pa iekšējām saitēm.
2. **Filtrs:** URL, kas izskatās pēc produkta (`/produkts/`, `/prece/`, `/product/`,
   `/veikals/`, `/noma/` u.c.). Ja heiristika neatrod, skripts izdrukā atrastos URL,
   lai vari norādīt `--product-re`.
3. **Attēla pārbaude:** meklē `og:image` un galerijas attēlus, izlaižot logo/ikonas;
   ja atrod tikai placeholder vai neko — skaita kā **bez foto**.

Ja rezultāts izskatās aizdomīgs (piem., 0 produktu), palaid ar `--limit 5` un
paskaties, ko tas raksta — parasti pietiek pielāgot `--product-re`.
