#!/usr/bin/env python3
"""Kopīgā loģika darbību žurnālam: ceļi, normalizēšana, ierakstu lasīšana."""
import json
import os
import re
import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path

FAILS = "zurnals.jsonl"
MARKERIS = "pedejais-apskats.json"

# Lauki, kurus vērtē 1-5 skalā. Ja nav norādīts, atskaitē lieto NOKLUSEJUMS.
SKALAS = ("atkartojamiba", "digitalitate", "spriedums", "kaitinajums")
NOKLUSEJUMS = 3


def datu_mape() -> Path:
    """1) $DARBIBU_ZURNALS_DIR  2) <git repo sakne>/darbibu-zurnals  3) ~/darbibu-zurnals"""
    no_vides = os.environ.get("DARBIBU_ZURNALS_DIR")
    if no_vides:
        mape = Path(no_vides).expanduser()
    else:
        mape = None
        try:
            sakne = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, timeout=5,
            )
            if sakne.returncode == 0 and sakne.stdout.strip():
                mape = Path(sakne.stdout.strip()) / "darbibu-zurnals"
        except (OSError, subprocess.SubprocessError):
            mape = None
        if mape is None:
            mape = Path.home() / "darbibu-zurnals"
    mape.mkdir(parents=True, exist_ok=True)
    return mape


def zurnala_cels() -> Path:
    return datu_mape() / FAILS


def markera_cels() -> Path:
    return datu_mape() / MARKERIS


def atslega(teksts: str) -> str:
    """Normalizē darbības nosaukumu grupēšanas atslēgā (bez garumzīmēm, ar defisēm)."""
    bez_diakritikas = "".join(
        z for z in unicodedata.normalize("NFKD", teksts.lower())
        if not unicodedata.combining(z)
    )
    tirs = re.sub(r"[^a-z0-9]+", "-", bez_diakritikas).strip("-")
    return "-".join(tirs.split("-")[:4]) or "nezinama-darbiba"


def lasit(sakums=None, beigas=None):
    """Ielasa ierakstus. sakums/beigas -> datetime.date vai None."""
    cels = zurnala_cels()
    if not cels.exists():
        return []
    ieraksti = []
    for nr, rinda in enumerate(cels.read_text(encoding="utf-8").splitlines(), 1):
        rinda = rinda.strip()
        if not rinda:
            continue
        try:
            ier = json.loads(rinda)
        except json.JSONDecodeError:
            print(f"BRIDINAJUMS: bojata rinda {nr} failā {cels} — izlaista")
            continue
        d = ier.get("datums")
        if not d:
            continue
        try:
            dat = datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            continue
        if sakums and dat < sakums:
            continue
        if beigas and dat > beigas:
            continue
        ier["_datums"] = dat
        ieraksti.append(ier)
    return ieraksti


def skala(ieraksts, lauks):
    """1-5 vērtība ar noklusējumu un ierobežojumu."""
    v = ieraksts.get(lauks)
    if v is None:
        return NOKLUSEJUMS
    try:
        return max(1, min(5, int(v)))
    except (TypeError, ValueError):
        return NOKLUSEJUMS
