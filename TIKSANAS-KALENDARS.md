# 🗓️ Tikšanos pierakstīšana kalendārā

Vienošanās par to, kā Māris padod tikšanās tekstā un Claude tās ieraksta kalendārā.

---

## 1. Izvēlētais kalendārs

**`maris.pelekzirnis@gmail.com`** — Google Calendar primārais kalendārs, laika josla **Europe/Riga**.

Kāpēc tieši šis:

| Kalendārs | ID | Rakstīt? | Piezīme |
|---|---|---|---|
| **maris.pelekzirnis@gmail.com** | `maris.pelekzirnis@gmail.com` | ✅ jā | Primārais, Europe/Riga, pieejams gan telefonā, gan datorā |
| Brīvdienas Latvijā | `lv.latvian#holiday@...` | ❌ nē | Google sistēmas kalendārs |
| Mākslīgā Intelekta apmācības | `djha8q6qv5p89ic9...@import...` | ❌ nē | Importēts (ICS) — tikai lasāms |
| MI rīku un aģentu izmantošana | `39j14e708b25j6c5...@import...` | ❌ nē | Importēts (ICS) — tikai lasāms |
| (DELETED) ×2 | `6io08a8...`, `foa2eut...` | ❌ nē | Miruši importi |

Visi pārējie kalendāri ir **importēti vai sistēmas kalendāri — tajos ierakstīt nav iespējams**.
Tāpēc viss iet primārajā, un tur pašam Claude ir gan rakstīšana, gan lasīšana (vēsture, meklēšana, labošana, dzēšana).

---

## 2. Kā Māris padod tikšanos

Pietiek ar vienu teikumu brīvā formā, piemēram:

- `otrdien 14:00 tikšanās ar Cramo par nomas tehniku`
- `rīt 9:30 zvans ar Brokk pārstāvi, 30 min`
- `12. septembrī 11:00 objekta apskate Ulbrokā, 2h`

Ja kaut kas nav pateikts, Claude pieņem **noklusējumus** (sk. 3. punktu) un ierakstā pasaka, ko pieņēma.
Jautājumus uzdod tikai tad, ja bez atbildes ieraksts būtu nepareizs (piem. divdomīgs datums).

---

## 3. Noklusējumi

| Lauks | Noklusējums |
|---|---|
| Kalendārs | `maris.pelekzirnis@gmail.com` |
| Laika josla | `Europe/Riga` |
| Ilgums | **1 h** (zvaniem, ja teikts "zvans" — 30 min) |
| Datums bez gada | Tuvākais nākotnes datums |
| Atgādinājumi | **popup 1 dienu iepriekš (1440 min)** + **popup 30 min iepriekš** |
| Statuss | Aizņemts (busy) |
| Vieta | Tikai tad, ja Māris to nosauc |
| Dalībnieki (uzaicinājumi) | **Netiek pievienoti automātiski** — e-pasta uzaicinājums aiziet tikai pēc tieša lūguma |

---

## 4. Ieraksta formāts

**Nosaukums:** `<Tēma> — <klients/partneris>`
(piem. `Nomas tehnikas pārrunas — Cramo`)

**Apraksts** (lai vēsture ir strukturēta un meklējama):

```
Tēma: nomas tehnikas piedāvājums 2026. gada sezonai
Dalībnieki: Māris, Cramo iepirkumu vadītājs
Vieta: Cramo birojs, Rīga
Piezīmes: paņemt līdzi BOMAG un Husqvarna cenu lapas

Ierakstīts no Claude Code sarunas 2026-08-25
#claude-log
```

Birka **`#claude-log`** aprakstā ir atslēga: pēc tās Claude vēlāk atrod visu, ko pats ir ierakstījis
(`search_events` / `list_events` ar `fullText: "#claude-log"`), un var parādīt vēsturi, labot vai dzēst.

---

## 5. Ko Claude atbild pēc ieraksta

Īsu apstiprinājumu — bez gariem paskaidrojumiem:

```
✅ Ierakstīts: Nomas tehnikas pārrunas — Cramo
   Otrdien, 2026-09-01, 14:00–15:00 (Europe/Riga)
   Atgādinājumi: 1 diena iepriekš + 30 min iepriekš
   Pieņēmu: ilgums 1 h (nebija norādīts)
```

---

## 6. Ko vēl var lūgt

- `ko man rāda kalendārs šonedēļ?` — Claude parāda ierakstus no primārā kalendāra
- `parādi visas tikšanās, ko tu esi ierakstījis` — meklē pēc `#claude-log`
- `pārcel Cramo tikšanos uz trešdienu 15:00` — labo esošo ierakstu
- `atcel rītdienas zvanu` — dzēš ierakstu (vienmēr vispirms nosauc, ko tieši dzēsīs)
