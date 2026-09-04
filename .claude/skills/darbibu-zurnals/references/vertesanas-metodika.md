# Vērtēšanas metodika

## Ieraksta lauki

| Lauks | Obligāts | Apraksts |
|-------|----------|----------|
| `darbiba` | jā | Ko darīja, cilvēka valodā |
| `atslega` | ieteicams | Grupēšanas atslēga no `kategorijas.md`. Bez tās skripts izveido no pirmajiem 4 vārdiem — un tad viena darbība sadalās vairākās grupās |
| `minutes` | ļoti ieteicams | Cik minūtes VIENĀ reizē (nevis kopā) |
| `reizes` | nē (1) | Cik reizes šī darbība notika |
| `riki` | nē | Word, OpenCart, Outlook, Excel, telefons, Lursoft… |
| `konteksts` | nē (darbs) | `darbs` vai `privati` |
| `avots` | nē (manuali) | `manuali`, `kalendars`, `gmail` |
| `piezimes` | nē | Kas tieši kaitināja vai aizķērās |

## 1–5 skalas

**`atkartojamiba`** — cik identiski norit katra reize.
1 = katra reize pilnīgi cita · 3 = tā pati forma, cits saturs · 5 = identiski soļi katru reizi

**`digitalitate`** — cik daudz notiek ekrānā/datos.
1 = fiziska darbība vai klātienes tikšanās · 3 = jaukti · 5 = pilnībā failos, sistēmās, tekstā

**`spriedums`** — cik maz vajadzīgs cilvēka spriedums (apgriezta skala!).
1 = kritisks cilvēka spriedums vai attiecības (sarunas par cenu, konflikti) · 3 = vajag pārbaudi · 5 = mehānisks, kļūdas cena zema

**`kaitinajums`** — cik nogurdinoši (neietekmē rangu, bet svarīgi motivācijai).
1 = patīk darīt · 5 = izsūc enerģiju

Ja nevar novērtēt — atstāj `null`. Noklusējums 3 un brīdinājums atskaitē ir godīgāks
par izdomātu skaitli.

## Aprēķins

```
automatizejamiba = (atkartojamiba + digitalitate + spriedums) / 3        # 1..5
dala              = (automatizejamiba - 1) / 4 * 0.8                     # 0..0.8
min_nedela        = kopejas_minutes / (perioda_dienas / 7)
ietaupijums       = min_nedela * dala
EUR_menesi        = ietaupijums / 60 * 4.33 * stundas_vertiba
```

**Kāpēc griesti 0.8:** pat ideāli automatizēta darbība prasa konteksta ievadi,
rezultāta pārbaudi un izņēmumu apstrādi. Solījums par 100% ietaupījumu ir melu.

**Prioritātes joslas** (pēc `ietaupijums` min/nedēļā):

| Josla | Slieksnis | Nozīme |
|-------|-----------|--------|
| AUGSTA | ≥ 60 | Automatizē tagad |
| VIDĒJA | 20–59 | Ieplāno šomēnes |
| ZEMA | 5–19 | Pietiek ar šablonu vai checklistu |
| IGNORĒ | < 5 | Automatizācija maksās vairāk nekā ietaupīs |

## Kad skaitļiem NEtici

- Periods < 7 dienas → nedēļas rādītāji ir ekstrapolēti no pārāk maza parauga.
- < 10 ieraksti kopā → nav modeļa, ir tikai anekdotes.
- Grupa ar vienu ierakstu un augstu rangu → visticamāk vienreizējs darbs, nevis modelis.
- Daudz `null` skalu → rangs ir aptuvens; pasaki to Mārim.
- Sezonalitāte: augusts un decembris nav tipiski mēneši būvniecības pārdošanā.
