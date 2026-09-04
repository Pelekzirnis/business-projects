---
name: darbibu-zurnals
description: Māra darbību žurnāls un periodiskais AI-optimizācijas apskats. Divi režīmi. (1) PIERAKSTĪŠANA — obligāti jāizmanto, kad Māris saka "pieraksti", "iemet žurnālā", "šodien darīju", "atkal taisīju", "log this", vai uzskaita, ar ko pavadīja laiku; ieraksts aiziet strukturētā JSONL žurnālā. (2) APSKATS — obligāti jāizmanto, kad Māris saka "nedēļas apskats", "mēneša apskats", "ko var automatizēt", "kur es tērēju laiku", "darbību analīze", "efektivizē manu darbu", "kas man atkārtojas", vai kad pēdējais apskats bijis vairāk nekā 7 dienas atpakaļ; sagrupē darbības, izrēķina ietaupījuma potenciālu stundās un EUR, un dod prioritizētu sarakstu ar konkrētiem AI/automatizācijas risinājumiem. Aktivizējas arī uz "ievāc no kalendāra", kad jāatjauno darbības no Google Calendar vai Gmail.
---

# Darbību žurnāls → AI optimizācija

Mērķis: uzkrāt to, ar ko Māris reāli pavada laiku, un pēc nedēļas/mēneša
pateikt, **kuras 1–3 darbības ir vērts automatizēt vispirms** un ar ko tieši.

Skripti dara matemātiku (grupēšana, min/nedēļā, EUR). Tu dari spriedumu
(kurš risinājums der, kas jāizmet vispār). Nekad neizdomā skaitļus — palaid skriptu.

## Ceļi

Skripti: `.claude/skills/darbibu-zurnals/scripts/`
Dati: `$DARBIBU_ZURNALS_DIR`, citādi `<repo sakne>/darbibu-zurnals/`, citādi `~/darbibu-zurnals/`.
Žurnāls: `zurnals.jsonl` (viens JSON objekts rindā, append-only).

---

## REŽĪMS 1 — PIERAKSTĪŠANA

Jābūt ātram. Māris iemet vienu rindiņu; tu neuzdod vairāk par vienu jautājumu.

**Solis 1.** Izparsē no teksta: ko darīja, cik ilgi, cik reizes, ar kādiem rīkiem.

**Solis 2.** Izvēlies `atslega` no `references/kategorijas.md`. Šis ir vissvarīgākais
solis — ja atslēgas atšķiras, viena darbība sadalās vairākās grupās un apskats melo.
Ja neviena esošā atslēga neder, izveido jaunu (mazie burti, bez garumzīmēm, ar defisēm)
un pieraksti to `references/kategorijas.md`.

**Solis 3.** Novērtē 1–5 skalas (`references/vertesanas-metodika.md`). Ja no teksta
nevar spriest, atstāj lauku `null` — skripts liks noklusējumu 3 un atskaitē to atzīmēs.
Nemēģini uzminēt precīzi; labāk `null` nekā izdomāts.

**Solis 4.** Pievieno:

```bash
echo '{"darbiba":"Web apraksts OpenCart precei","atslega":"web-apraksts",
"minutes":25,"reizes":3,"riki":["OpenCart"],"atkartojamiba":5,"digitalitate":5,
"spriedums":4,"kaitinajums":3,"konteksts":"darbs"}' | \
  python3 .claude/skills/darbibu-zurnals/scripts/pieraksti.py
```

Vairākus ierakstus vienā reizē — padod JSON masīvu (`[{...},{...}]`).

**Solis 5.** Apstiprini vienā rindā: `Pierakstīts: web-apraksts, 25 min x3.` Nekādu analīzi.
Analīze notiek apskatā, ne pierakstīšanas brīdī.

### Dienas beigu dump
Ja Māris uzskaita vairākas lietas ("šodien: 3 piedāvājumi, 2h zvani, akts Bergam"),
sadali tās atsevišķos ierakstos un pievieno vienā izsaukumā kā masīvu.

### Ievākšana no kalendāra un pasta
Kad Māris saka "ievāc no kalendāra" vai žurnāls ir tukšs, bet vajag apskatu:
1. `mcp__Google_Calendar__list_events` par periodu → katrs pasākums ar ilgumu = ieraksts, `avots: "kalendars"`.
2. `mcp__Gmail__search_threads` ar `from:maris.pelekzirnis@technitis.lv` → atkārtojošies izejošie e-pasti = ieraksts, `avots: "gmail"`.
3. Parādi Mārim sarakstu **pirms** pievienošanas un ļauj izsvītrot.

Šis ir apzināti pirmais solis, ja Māris saka, ka nespēs katru dienu pierakstīt —
pasīvie avoti nomirst retāk nekā disciplīna.

---

## REŽĪMS 2 — APSKATS

**Solis 1.** Palaid skriptu. Nedēļai:

```bash
python3 .claude/skills/darbibu-zurnals/scripts/atskaite.py --nedela --stundas-vertiba 25
```

Mēnesim: `--menesis`. Konkrētam periodam: `--no 2026-08-01 --lidz 2026-08-31`.
Kad apskats ir pabeigts un nodots Mārim, palaid vēlreiz ar `--atzimet`, lai fiksētu datumu.

**Solis 2.** Pārbaudi atslēgu higiēnu, pirms tici skaitļiem:

```bash
python3 .claude/skills/darbibu-zurnals/scripts/sapludinat.py --atslegas
```

Ja redzi divas atslēgas, kas ir viena darbība — sapludini un palaid atskaiti vēlreiz:
`sapludinat.py --uz komercpiedavajums --no piedavajums-word piedavajums-klientam`

**Solis 3.** Katram TOP kandidātam izlem risinājumu pēc `references/risinajumu-karte.md`.
Secība ir stingra un šajā kārtībā:
1. **Vai to var nedarīt vispār?** (izmest, atteikt, retāk) — nulles izmaksas, lielākais ieguvums.
2. **Vai to var deleģēt cilvēkam?**
3. **Vai pietiek ar šablonu / checklistu?** (nav AI)
4. **Vai der esošs Technitis skill?** Pārbaudi — daudzi jau eksistē (piedāvājumi, akti, web apraksti, līgumi).
5. **Vajag jaunu skillu / Claude Projektu?**
6. **Vajag Make.com vai Zapier scenāriju?** (kad jāsavieno sistēmas bez cilvēka)
7. **Vajag skriptu?**

Nekad neiesaki jaunu būvēt, ja 1.–4. punkts to atrisina.

**Solis 4.** Izvadi atskaiti šādā formātā — tas ir COACH režīms, ievēro Māra stila prasības:

```
## Periods un fakti
[skripta kopsavilkuma skaitļi — h/nedēļā, EUR/mēnesī, ierakstu skaits]

## Kas jau strādā labi
[1-3 konkrētas lietas: kur laiks jau ir zems attiecībā pret vērtību,
 kur iepriekšējais automatizācijas solis nostrādājis. Konkrēti, ne vispārīgi.]

## TOP 3 automatizācijas kandidāti
Katram:
- Darbība + cik min/nedēļā + cik EUR/mēnesī
- Risinājums: [konkrēts — kurš skill / kurš Make scenārijs / kurš šablons]
- Ieviešanas darbs: S (<1h) / M (1 diena) / L (vairākas dienas)
- Atmaksāšanās: [ietaupījums h/mēn pret ieviešanas darbu]

## Ko izmest, nevis automatizēt
[darbības ar zemu vērtību — automatizēt nevajadzīgu darbu ir sliktākais variants]

## Datu kvalitāte
[skripta brīdinājumi — cik ierakstiem trūkst laika vai skalu]

## NĀKAMAIS SOLIS
[VIENA darbība šai nedēļai. Ne saraksts. Konkrēta un pabeidzama.]
```

**Solis 5.** Verdikts vienā rindā: `Automatizē tagad / Vāc vēl datus / Nav ko automatizēt`.

### Ja datu par maz
Ja žurnālā < 10 ieraksti vai periods < 7 dienas — pasaki to tieši, neizliecies par analīzi.
Nākamais solis tad ir "vāc datus", nevis "būvē automatizāciju". Piedāvā ievākšanu no kalendāra.

---

## Periodiskā palaišana

Māris apskatu neatcerēsies. Piedāvā uzstādīt vienu no šiem:
- **Claude Routine** (`create_trigger`): katru piektdienu 15:00 pēc Latvijas laika = cron `0 12 * * 5` (UTC vasarā) / `0 13 * * 5` (ziemā). Prompts: "Palaid darbibu-zurnals nedēļas apskatu."
- **`/loop`** garākiem periodiem tajā pašā sesijā.
- Katras sesijas sākumā: `pieraksti.py --statuss` parāda, cik dienas kopš pēdējā apskata. Ja > 7 — piedāvā apskatu.

## Robežas

- Nepievieno ierakstus par Māra veselību vai finansēm bez tieša lūguma.
- Nepublicē žurnāla saturu ārpus repo (nav e-pastos, nav artifaktos) bez atļaujas.
- Žurnāls ir append-only. Vienīgais atļautais rediģēšanas ceļš ir `sapludinat.py`.
