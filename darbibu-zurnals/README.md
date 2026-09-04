# Darbību žurnāls

Šeit dzīvo dati skillam `.claude/skills/darbibu-zurnals`.

| Fails | Saturs |
|-------|--------|
| `zurnals.jsonl` | Ieraksti, viens JSON objekts rindā. Append-only. Rodas pēc pirmās pierakstīšanas. |
| `pedejais-apskats.json` | Kad pēdējo reizi veikts apskats. |

## Ātrā lietošana

```bash
# Pierakstīt
echo '{"darbiba":"Web apraksts OpenCart precei","atslega":"web-apraksts","minutes":25,"reizes":3}' \
  | python3 .claude/skills/darbibu-zurnals/scripts/pieraksti.py

# Kur esmu
python3 .claude/skills/darbibu-zurnals/scripts/pieraksti.py --statuss

# Nedēļas apskats
python3 .claude/skills/darbibu-zurnals/scripts/atskaite.py --nedela --stundas-vertiba 25

# Mēneša apskats un datuma fiksēšana
python3 .claude/skills/darbibu-zurnals/scripts/atskaite.py --menesis --atzimet

# Atslēgu higiēna
python3 .claude/skills/darbibu-zurnals/scripts/sapludinat.py --atslegas
```

Praksē to nav jādara ar roku — pasaki Claude "pieraksti: ..." vai "nedēļas apskats",
un skills palaiž skriptus pats.

## Citur glabāt

`export DARBIBU_ZURNALS_DIR=~/darbibu-zurnals` — tad dati paliek ārpus repo.
