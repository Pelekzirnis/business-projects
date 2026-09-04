#!/usr/bin/env python3
"""Sapludina atslēgas žurnālā — kad viena un tā pati darbība ir pierakstīta
ar dažādiem nosaukumiem un tāpēc sadalījusies vairākās grupās.

  python3 sapludinat.py --uz komercpiedavajums --no sagatavot-komercpiedavajumu-word-formata sagatavot-komercpiedavajumu-klientam-bomag
  python3 sapludinat.py --atslegas          # parāda visas esošās atslēgas
"""
import argparse
import json
import sys
from collections import Counter

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from zurnals import lasit, zurnala_cels  # noqa: E402


def main():
    p = argparse.ArgumentParser(description="Sapludina vai uzskaita žurnāla atslēgas")
    p.add_argument("--atslegas", action="store_true", help="Uzskaita esošās atslēgas ar ierakstu skaitu")
    p.add_argument("--uz", help="Mērķa atslēga")
    p.add_argument("--no", dest="avoti", nargs="+", help="Atslēgas, ko pārsaukt uz mērķa atslēgu")
    args = p.parse_args()

    ieraksti = lasit()
    if args.atslegas or not (args.uz and args.avoti):
        if not (args.uz and args.avoti) and not args.atslegas:
            print("Norādi --uz un --no, vai --atslegas.\n", file=sys.stderr)
        skaits = Counter(i.get("atslega", "?") for i in ieraksti)
        for atsl, n in skaits.most_common():
            piemers = next(i["darbiba"] for i in ieraksti if i.get("atslega") == atsl)
            print(f"{n:4}  {atsl:45} {piemers[:50]}")
        return 0 if args.atslegas else 1

    avoti = set(args.avoti)
    cels = zurnala_cels()
    rindas, mainitas = [], 0
    for rinda in cels.read_text(encoding="utf-8").splitlines():
        if not rinda.strip():
            continue
        ier = json.loads(rinda)
        if ier.get("atslega") in avoti:
            ier["atslega"] = args.uz
            mainitas += 1
        rindas.append(json.dumps(ier, ensure_ascii=False))
    cels.write_text("\n".join(rindas) + "\n", encoding="utf-8")
    print(f"Pārsauktas {mainitas} rindas uz '{args.uz}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
