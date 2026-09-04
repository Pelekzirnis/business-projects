#!/usr/bin/env python3
"""Pievieno vienu vai vairākus ierakstus darbību žurnālam.

Lietošana:
  echo '{"darbiba":"...","minutes":25}' | python3 pieraksti.py
  python3 pieraksti.py --json '[{"darbiba":"..."},{"darbiba":"..."}]'
  python3 pieraksti.py --statuss
"""
import argparse
import json
import sys
import uuid
from datetime import datetime, date

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from zurnals import atslega, lasit, markera_cels, zurnala_cels, SKALAS  # noqa: E402

ATLAUTIE = {
    "darbiba", "atslega", "konteksts", "minutes", "reizes", "riki",
    "atkartojamiba", "digitalitate", "spriedums", "kaitinajums",
    "avots", "piezimes", "datums", "laiks", "id",
}


def sagatavot(ier):
    if not isinstance(ier, dict):
        raise ValueError("Ierakstam jābūt JSON objektam")
    darbiba = str(ier.get("darbiba", "")).strip()
    if not darbiba:
        raise ValueError("Obligāts lauks 'darbiba' trūkst vai ir tukšs")

    nezinami = set(ier) - ATLAUTIE
    if nezinami:
        raise ValueError(f"Nezināmi lauki: {', '.join(sorted(nezinami))}")

    tagad = datetime.now()
    datums = str(ier.get("datums") or tagad.date().isoformat())
    try:
        datetime.strptime(datums, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Nederīgs datums '{datums}' — vajag GGGG-MM-DD")

    minutes = ier.get("minutes")
    if minutes is not None:
        try:
            minutes = max(0, int(minutes))
        except (TypeError, ValueError):
            raise ValueError(f"'minutes' jābūt skaitlim, nevis {minutes!r}")

    reizes = ier.get("reizes", 1)
    try:
        reizes = max(1, int(reizes))
    except (TypeError, ValueError):
        raise ValueError(f"'reizes' jābūt skaitlim, nevis {reizes!r}")

    riki = ier.get("riki") or []
    if isinstance(riki, str):
        riki = [r.strip() for r in riki.split(",") if r.strip()]

    jauns = {
        "id": ier.get("id") or f"{datums.replace('-', '')}-{uuid.uuid4().hex[:6]}",
        "datums": datums,
        "laiks": ier.get("laiks") or tagad.isoformat(timespec="minutes"),
        "darbiba": darbiba,
        "atslega": ier.get("atslega") or atslega(darbiba),
        "konteksts": ier.get("konteksts") or "darbs",
        "minutes": minutes,
        "reizes": reizes,
        "riki": riki,
        "avots": ier.get("avots") or "manuali",
        "piezimes": ier.get("piezimes") or "",
    }
    for lauks in SKALAS:
        v = ier.get(lauks)
        if v is not None:
            try:
                v = int(v)
            except (TypeError, ValueError):
                raise ValueError(f"'{lauks}' jābūt veselam skaitlim 1-5, nevis {v!r}")
            if not 1 <= v <= 5:
                raise ValueError(f"'{lauks}' jābūt robežās 1-5, nevis {v}")
        jauns[lauks] = v
    return jauns


def main():
    p = argparse.ArgumentParser(description="Pievieno ierakstus darbību žurnālam")
    p.add_argument("--json", help="JSON objekts vai masīvs (citādi lasa no stdin)")
    p.add_argument("--statuss", action="store_true", help="Parāda žurnāla kopsavilkumu un neko nepievieno")
    args = p.parse_args()

    if args.statuss:
        ieraksti = lasit()
        cels = zurnala_cels()
        print(f"Žurnāls: {cels}")
        print(f"Ieraksti: {len(ieraksti)}")
        if ieraksti:
            print(f"Periods: {min(i['_datums'] for i in ieraksti)} .. {max(i['_datums'] for i in ieraksti)}")
        m = markera_cels()
        if m.exists():
            dati = json.loads(m.read_text(encoding="utf-8"))
            pedejais = datetime.strptime(dati["pedejais_apskats"], "%Y-%m-%d").date()
            print(f"Pēdējais apskats: {pedejais} ({(date.today() - pedejais).days} dienas atpakaļ)")
        else:
            print("Pēdējais apskats: nekad")
        return 0

    neapstradats = args.json if args.json else sys.stdin.read()
    if not neapstradats.strip():
        print("KĻŪDA: nav ievaddatu (padod --json vai stdin)", file=sys.stderr)
        return 1
    try:
        dati = json.loads(neapstradats)
    except json.JSONDecodeError as e:
        print(f"KĻŪDA: nederīgs JSON — {e}", file=sys.stderr)
        return 1

    saraksts = dati if isinstance(dati, list) else [dati]
    try:
        gatavie = [sagatavot(i) for i in saraksts]
    except ValueError as e:
        print(f"KĻŪDA: {e}", file=sys.stderr)
        return 1

    cels = zurnala_cels()
    with cels.open("a", encoding="utf-8") as f:
        for g in gatavie:
            f.write(json.dumps(g, ensure_ascii=False) + "\n")

    print(f"Pievienoti {len(gatavie)} ieraksti -> {cels}")
    for g in gatavie:
        mins = f"{g['minutes']} min" if g["minutes"] is not None else "laiks nenorādīts"
        print(f"  [{g['atslega']}] {g['darbiba']} ({mins}, x{g['reizes']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
