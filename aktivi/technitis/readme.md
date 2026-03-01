# Technitis AI Piedāvājumu Sistēma

Projekts izstrādāts lai automatizētu Technitis Latvia pārdošanas piedāvājumu sagatavošanu, samazinot laiku no ~45 minūtēm līdz 5–10 minūtēm uz vienu piedāvājumu.

---

## Problēma

Katrs piedāvājums tika gatavots manuāli – produktu specs, cenas, finansējums, klienta dati – viss no nulles katru reizi. Ar plašu produktu katalogu (miniekskavatatori, iekrāvēji, ģeneratori, kompresori, sildītāji, slīpmašīnas, demontāžas roboti) un mainīgām komplektācijām (~10 opcijas vienam modelim) process bija laikietilpīgs un nekonsekvents.

---

## Risinājums

**Google Sheets + Claude AI + Google Docs → PDF**

Trīs komponenti:

1. **Produktu datubāze (Google Sheets)** – strukturēta tabula ar bāzes modeļiem, opcijām un fiksētām cenām
2. **AI prompt veidne (Claude)** – standartizēts prompt kas no Sheets datiem ģenerē gatavu piedāvājuma tekstu
3. **Dokumenta veidne (Google Docs)** – Technitis vizuālā identitāte, eksports PDF formātā

---

## Produktu kategorijas

| Kategorija | Tips |
|---|---|
| Miniekskavatatori | Lietoti |
| GEHL Kompaktiekrāvēji | Jauni + Lietoti |
| Kompaktiekrāvēju uzkares | Jauni |
| Ģeneratori | Jauni |
| Kompresori | Jauni |
| Thermamax sildītāji | Jauni |
| Dr. Schulze slīpmašīnas + sūcēji | Jauni |
| Brokk demontāžas roboti | Jauni |

---

## Sheets struktūra

Katra kategorija satur 3 cilnes:

**Cilne 1 – Bāzes modeļi**
```
Modelis | Bāzes cena EUR+PVN | Dzinējs/Jauda | Galvenie parametri | Finansējums | Piegāde | Statuss
```

**Cilne 2 – Opcijas**
```
Modelis | Opcijas nosaukums | Cena +EUR | Kategorija | Piezīmes
```

**Cilne 3 – Veidnes teksts**
```
Fiksēts intro/outro teksts katram modelim
```

---

## Prompt veidne

```
Tu esi Technitis Latvia pārdošanas speciālists.
Sagatavo profesionālu piedāvājumu latviešu valodā.

Klients: [uzņēmuma nosaukums]
Kontaktpersona: [vārds, telefons]
Produkts: [nosaukums]
Statuss: [Jauns / Lietots]
Bāzes cena: [summa] EUR + PVN
Izvēlētās opcijas: [opcija 1 +EUR, opcija 2 +EUR]
Galīgā cena: [summa] EUR + PVN
Tehniskie parametri: [no Sheets]
Finansējums: [ja ir]
Piegādes laiks: [X nedēļas]

Struktūra:
1. Īss ievads (1-2 teikumi par Technitis)
2. Produkta apraksts ar galvenajiem parametriem
3. Izvēlētā komplektācija un opcijas
4. Cena un finansējuma iespējas
5. Servisa garantija
6. Noslēgums ar aicinājumu sazināties

Tonis: profesionāls, konkrēts, bez liekajiem vārdiem.
```

---

## Darba plūsma

```
1. Klients pieprasa piedāvājumu
2. Atver Google Sheets → atrod modeli
3. Kopē bāzes datus + izvēlas opcijas
4. Ieliek prompt Claude
5. Claude ģenerē piedāvājuma tekstu
6. Ieliec Google Docs veidnē
7. Eksportē PDF → nosūta klientam
```

**Rezultāts:** 45 min → 5–10 min uz piedāvājumu

---

## Tehnoloģijas

- Google Sheets – produktu datubāze
- Claude AI (Anthropic) – teksta ģenerēšana
- Google Docs – dokumenta veidne
- PDF eksports – klientam nosūtāmais formāts

---

## Statuss

- [x] Projekta koncepcija
- [x] Sheets struktūra izstrādāta
- [ ] Produktu datubāze aizpildīta
- [ ] Prompt veidnes testētas
- [ ] Pirmais reālais piedāvājums ģenerēts
- [ ] Laika ietaupījums izmērīts un dokumentēts

---

## Portfolio vērtība

Šis projekts kalpo kā **dzīvs portfolio piemērs** AI konsultāciju pakalpojumam. Mērāms rezultāts (laiks, konversija) tiks izmantots kā pierādījums citiem uzņēmumiem – zobārstiem, juristiem, nekustamā īpašuma aģentūrām – kuriem tiek piedāvāts līdzīgs risinājums.

---

*SIA Technitis Latvia | Berģi, Garkalnes novads | riga@technitis.lv*
