# No darbības uz risinājumu

Secība ir svarīgāka par tehnoloģiju. Vienmēr ej no augšas uz leju.

## 0. Izmest
**Kad:** darbība ir zemas vērtības, notiek pēc inerces, neviens neprasa rezultātu.
**Jautājums:** ja to nedarītu 2 nedēļas, kas notiktu?
**Automatizēt nevajadzīgu darbu nozīmē padarīt to mūžīgu.**

## 1. Deleģēt
**Kad:** darbība ir vērtīga, bet neprasa tieši Māra pieredzi.
Kolēģis, birojs, piegādātājs (piem., specifikācijas var prasīt ražotāja pārstāvim).

## 2. Šablons vai checklist
**Kad:** `atkartojamiba` ≥ 4, bet notiek retāk par 1x nedēļā.
Word šablons, Gmail canned response, saglabāts teksts. Bez AI. Ieviešana < 1h.

## 3. Esošs Technitis skill
**Pārbaudi vienmēr, pirms būvē jaunu:**

| Darbība | Skill |
|---------|-------|
| Komercpiedāvājumi | `technitis-offer` |
| PN akti | `technitis-pn-akts` |
| Līgumi | `technitis-ligums`, `technitis-nomas-ligums` |
| Web apraksti | `technitis-web-apraksts-bold`, `technitis-lv-web-apraksts-teksts-bez-bold` |
| Sludinājumi | `technitis-ss-com` |
| Nedēļas reports | `technitis-weekly-report` |
| Produktu jautājumi | `technitis-centrs` → nozares aģenti 01–18 |
| Promtu būve | `m-prompt-builder`, `karpathy-promt-arhitekts` |

Ja skills eksistē, bet Māris to nelieto — **problēma nav automatizācijā, bet ieradumā**.
Tas ir cits nākamais solis: trigeris, nevis jauns kods.

## 4. Jauns skill vai Claude Projekts
**Kad:** atkārtojas ≥ 2x nedēļā, ir skaidra ievade un izvade, esošs skill neder.
**Ieviešana:** S–M. Izmanto `skill-creator`.
**Brīdinājums:** skills, ko lieto 1x mēnesī, mirst. Zem 2x/nedēļā — labāk šablons.

## 5. Make.com vai Zapier scenārijs
**Kad:** jāsavieno divas sistēmas bez cilvēka klātbūtnes — e-pasts → CRM, forma → aprēķins,
atgādinājumi pēc grafika, datu pārnese starp Gmail/Sheets/Notion.
**Šajā sesijā pieejami MCP:** Make un Zapier — scenāriju var uzbūvēt uzreiz.
**Ieviešana:** M. **Brīdinājums:** klusa kļūme scenārijā ir bīstamāka par manuālu darbu —
vienmēr paredzi kļūdas paziņojumu.

## 6. Skripts
**Kad:** datu apstrāde, failu pārsaukšana, Excel, PDF izvilkšana.
**Ieviešana:** S–M. Vienreiz uzrakstīts, strādā gadiem.

## 7. Claude Routine (`create_trigger`)
**Kad:** darbība ir ne tikai atkārtojama, bet arī periodiska (piektdienas reports,
pirmdienas follow-up saraksts). Sapāro ar 3.–6. punktu — Routine palaiž risinājumu.

---

## Ieviešanas darba skala

| Apzīmējums | Laiks | Piemēri |
|------------|-------|---------|
| S | < 1h | Šablons, Gmail filtrs, esoša skilla pielāgošana |
| M | 1 diena | Jauns skill, Make scenārijs, skripts |
| L | vairākas dienas | Sistēmu integrācija, datubāze, vairāku soļu pipeline |

**Atmaksāšanās slieksnis:** ieviešanas laiks jāatpelna 8 nedēļās.
S atmaksājas jau pie 8 min/nedēļā. M (8h) prasa ≥ 60 min/nedēļā. L — tikai AUGSTAJAI joslai.
