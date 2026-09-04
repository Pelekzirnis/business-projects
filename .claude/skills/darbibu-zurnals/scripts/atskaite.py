#!/usr/bin/env python3
"""Apkopo darbību žurnālu un aprēķina automatizācijas potenciālu.

Skripts dara TIKAI matemātiku (grupēšana, min/nedēļā, ietaupījums, EUR).
Spriedumu — kurš AI risinājums der — pieņem Claude, balstoties uz šo izvadi.

Lietošana:
  python3 atskaite.py --nedela
  python3 atskaite.py --menesis --stundas-vertiba 30
  python3 atskaite.py --no 2026-08-01 --lidz 2026-08-31 --json
  python3 atskaite.py --menesis --atzimet
"""
import argparse
import json
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from zurnals import lasit, markera_cels, skala, NOKLUSEJUMS  # noqa: E402

# Cik lielu daļu no darbības reāli var noņemt pat pie ideāla automatizācijas
# rādītāja. 0.8 — jo vienmēr paliek pārbaude, konteksta ievade un izņēmumi.
GRIESTI = 0.8

JOSLAS = (
    (60, "AUGSTA", "Automatizē tagad"),
    (20, "VIDĒJA", "Ieplāno šomēnes"),
    (5, "ZEMA", "Pietiek ar šablonu vai checklist"),
    (0, "IGNORĒ", "Nav vērts pūļu"),
)


def josla(min_nedela):
    for slieksnis, nosaukums, darbiba in JOSLAS:
        if min_nedela >= slieksnis:
            return nosaukums, darbiba
    return "IGNORĒ", "Nav vērts pūļu"


def apkopot(ieraksti, dienas, stundas_vertiba):
    grupas = defaultdict(list)
    for i in ieraksti:
        grupas[i.get("atslega") or "nezinama-darbiba"].append(i)

    nedelas = max(dienas / 7.0, 1 / 7.0)
    rezultati = []
    for atsl, saraksts in grupas.items():
        reizes = sum(int(i.get("reizes") or 1) for i in saraksts)
        ar_laiku = [i for i in saraksts if i.get("minutes") is not None]
        minutes_kopa = sum(int(i["minutes"]) * int(i.get("reizes") or 1) for i in ar_laiku)
        # Ierakstiem bez laika piemēro grupas vidējo, lai tie nepazustu no aprēķina.
        if ar_laiku and len(ar_laiku) < len(saraksts):
            vid = minutes_kopa / max(sum(int(i.get("reizes") or 1) for i in ar_laiku), 1)
            bez_laika = sum(int(i.get("reizes") or 1) for i in saraksts if i.get("minutes") is None)
            minutes_kopa += vid * bez_laika

        vid_skala = {
            lauks: sum(skala(i, lauks) for i in saraksts) / len(saraksts)
            for lauks in ("atkartojamiba", "digitalitate", "spriedums", "kaitinajums")
        }
        # Automatizējamība: cik darbība padodas mašīnai (1-5).
        a_score = (vid_skala["atkartojamiba"] + vid_skala["digitalitate"] + vid_skala["spriedums"]) / 3
        dala = (a_score - 1) / 4 * GRIESTI  # 0..0.8

        min_nedela = minutes_kopa / nedelas
        ietaupijums = min_nedela * dala
        nosaukums, ieteikums = josla(ietaupijums)

        rezultati.append({
            "atslega": atsl,
            "darbiba": saraksts[-1].get("darbiba", atsl),
            "varianti": sorted({i.get("darbiba", "") for i in saraksts})[:5],
            "reizes": reizes,
            "reizes_nedela": round(reizes / nedelas, 1),
            "minutes_kopa": round(minutes_kopa),
            "min_nedela": round(min_nedela),
            "riki": sorted({r for i in saraksts for r in (i.get("riki") or [])}),
            "konteksts": saraksts[-1].get("konteksts", "darbs"),
            "atkartojamiba": round(vid_skala["atkartojamiba"], 1),
            "digitalitate": round(vid_skala["digitalitate"], 1),
            "spriedums": round(vid_skala["spriedums"], 1),
            "kaitinajums": round(vid_skala["kaitinajums"], 1),
            "automatizejamiba": round(a_score, 1),
            "ietaupijums_min_nedela": round(ietaupijums),
            "ietaupijums_h_menesi": round(ietaupijums * 4.33 / 60, 1),
            "ietaupijums_eur_menesi": round(ietaupijums * 4.33 / 60 * stundas_vertiba),
            "prioritate": nosaukums,
            "ieteikums": ieteikums,
            "bez_laika": sum(1 for i in saraksts if i.get("minutes") is None),
            "noklusetas_skalas": sum(
                1 for i in saraksts
                if all(i.get(l) is None for l in ("atkartojamiba", "digitalitate", "spriedums"))
            ),
        })

    rezultati.sort(key=lambda r: r["ietaupijums_min_nedela"], reverse=True)
    return rezultati


def markdown(rez, sakums, beigas, dienas, ieraksti, stundas_vertiba):
    r = []
    r.append(f"# Darbību apskats: {sakums} .. {beigas} ({dienas} dienas)")
    r.append("")
    kopa_min = sum(x["minutes_kopa"] for x in rez)
    kopa_ietaup = sum(x["ietaupijums_min_nedela"] for x in rez)
    kopa_eur = sum(x["ietaupijums_eur_menesi"] for x in rez)
    r.append(f"- Ieraksti: **{len(ieraksti)}**, unikālas darbības: **{len(rez)}**")
    r.append(f"- Uzskaitītais laiks: **{round(kopa_min/60, 1)} h** ({kopa_min} min)")
    r.append(f"- Teorētiskais ietaupījums: **{round(kopa_ietaup/60, 1)} h/nedēļā** "
             f"≈ **{round(kopa_ietaup*4.33/60, 1)} h/mēnesī** ≈ **{kopa_eur} EUR/mēnesī** "
             f"(pie {stundas_vertiba} EUR/h)")
    r.append("")
    r.append("## Rangs pēc automatizācijas potenciāla")
    r.append("")
    r.append("| # | Darbība | Reizes/ned | Min/ned | Autom. (1-5) | Ietaupījums min/ned | EUR/mēn | Prioritāte |")
    r.append("|---|---------|-----------:|--------:|-------------:|--------------------:|--------:|------------|")
    for n, x in enumerate(rez, 1):
        r.append(
            f"| {n} | {x['darbiba'][:52]} | {x['reizes_nedela']} | {x['min_nedela']} | "
            f"{x['automatizejamiba']} | {x['ietaupijums_min_nedela']} | "
            f"{x['ietaupijums_eur_menesi']} | {x['prioritate']} |"
        )
    r.append("")

    top = [x for x in rez if x["prioritate"] in ("AUGSTA", "VIDĒJA")][:5]
    if top:
        r.append("## Detaļas TOP kandidātiem")
        r.append("")
        for x in top:
            r.append(f"### {x['darbiba']}  `{x['atslega']}`")
            r.append(f"- Biežums: {x['reizes_nedela']}x/ned ({x['reizes']}x periodā), "
                     f"{x['min_nedela']} min/ned")
            r.append(f"- Atkārtojamība {x['atkartojamiba']} | Digitalitāte {x['digitalitate']} | "
                     f"Spriedums (5=nevajag cilvēku) {x['spriedums']} | Kaitinājums {x['kaitinajums']}")
            r.append(f"- Rīki: {', '.join(x['riki']) or '—'}")
            if len(x["varianti"]) > 1:
                r.append(f"- Varianti: {'; '.join(v for v in x['varianti'] if v)[:200]}")
            r.append(f"- Potenciāls: **{x['ietaupijums_h_menesi']} h/mēn** "
                     f"({x['ietaupijums_eur_menesi']} EUR) — {x['ieteikums']}")
            r.append("")

    bridinajumi = []
    bez_laika = sum(x["bez_laika"] for x in rez)
    if bez_laika:
        bridinajumi.append(f"{bez_laika} ierakstiem nav norādītas minūtes — laiks aprēķināts pēc grupas vidējā.")
    noklus = sum(x["noklusetas_skalas"] for x in rez)
    if noklus:
        bridinajumi.append(f"{noklus} ierakstiem nav novērtējuma skalu — lietots noklusējums {NOKLUSEJUMS}/5, "
                           "tāpēc to rangs ir aptuvens.")
    if dienas < 7:
        bridinajumi.append(f"Periods ir tikai {dienas} dienas — nedēļas rādītāji ir ekstrapolēti un nestabili.")
    if len(ieraksti) < 10:
        bridinajumi.append(f"Tikai {len(ieraksti)} ieraksti — par maz drošiem secinājumiem. Vāc vēl.")
    if bridinajumi:
        r.append("## Datu kvalitāte")
        r.append("")
        for b in bridinajumi:
            r.append(f"- {b}")
        r.append("")
    return "\n".join(r)


def main():
    p = argparse.ArgumentParser(description="Darbību žurnāla apskats un automatizācijas potenciāls")
    grupa = p.add_mutually_exclusive_group()
    grupa.add_argument("--nedela", action="store_true", help="Pēdējās 7 dienas")
    grupa.add_argument("--menesis", action="store_true", help="Pēdējās 30 dienas")
    grupa.add_argument("--viss", action="store_true", help="Viss žurnāls")
    p.add_argument("--no", dest="sakums", help="Sākuma datums GGGG-MM-DD")
    p.add_argument("--lidz", dest="beigas", help="Beigu datums GGGG-MM-DD")
    p.add_argument("--stundas-vertiba", type=float, default=25.0, help="EUR/h Māra laika vērtība (noklusējums 25)")
    p.add_argument("--json", action="store_true", help="Izvade JSON, nevis Markdown")
    p.add_argument("--atzimet", action="store_true", help="Atzīmē, ka apskats ir veikts (šodienas datums)")
    args = p.parse_args()

    sodien = date.today()
    if args.sakums:
        sakums = datetime.strptime(args.sakums, "%Y-%m-%d").date()
    elif args.menesis:
        sakums = sodien - timedelta(days=30)
    elif args.viss:
        sakums = None
    else:
        sakums = sodien - timedelta(days=7)
    beigas = datetime.strptime(args.beigas, "%Y-%m-%d").date() if args.beigas else sodien

    ieraksti = lasit(sakums, beigas)
    if not ieraksti:
        print("Žurnālā nav ierakstu izvēlētajā periodā. Sāc ar pieraksti.py.")
        return 0

    if sakums is None:
        sakums = min(i["_datums"] for i in ieraksti)
    dienas = max((beigas - sakums).days, 1)

    rez = apkopot(ieraksti, dienas, args.stundas_vertiba)

    if args.json:
        print(json.dumps({
            "sakums": sakums.isoformat(),
            "beigas": beigas.isoformat(),
            "dienas": dienas,
            "ierakstu_skaits": len(ieraksti),
            "stundas_vertiba": args.stundas_vertiba,
            "grupas": rez,
        }, ensure_ascii=False, indent=2))
    else:
        print(markdown(rez, sakums, beigas, dienas, ieraksti, args.stundas_vertiba))

    if args.atzimet:
        markera_cels().write_text(
            json.dumps({"pedejais_apskats": sodien.isoformat(),
                        "periods": [sakums.isoformat(), beigas.isoformat()],
                        "ierakstu_skaits": len(ieraksti)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
