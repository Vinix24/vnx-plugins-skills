#!/usr/bin/env python3
"""
pii_strip.py — Pseudonimisering voor interview-transcripten (lokaal, geen cloud)

Gebruik:
  Strip:    pii_strip.py strip   transcript.txt [--map mapping.json] [--out out.txt]
  Restore:  pii_strip.py restore transcript_anon.txt --map mapping.json [--out out.txt]

Drie detectielagen draaien op de ORIGINELE tekst (geen placeholder-interferentie):
  1. Regex        — bedragen, percentages, e-mail, telefoon, rekening/IBAN
  2. spaCy NER    — organisaties, locaties, bekende persoonsnames
  3. Voornamenlijst + hoofdletter-heuristiek — overige namen die NER mist
Alle matches worden gecombineerd en in één pass van achter naar voren vervangen.
"""

import argparse
import json
import re
import sys
from pathlib import Path

VENV_SPACY = Path.home() / "whisper/venv/lib"
for p in VENV_SPACY.glob("python*/site-packages"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import spacy

# ─── Ingebakken voornamenlijst ───────────────────────────────────────────────
DUTCH_FIRST_NAMES: set[str] = {n.lower() for n in {
    "Aaron","Adam","Alexander","Alexis","Arthur","Axel","Bas","Boris",
    "Bram","Bruno","Bryan","Carlos","Casper","Christiaan","Christian",
    "Daan","Daniel","David","Dennis","Diego","Diederik","Djibo","Dylan",
    "Edwin","Elias","Emil","Emile","Erik","Ethan","Ewout","Ferre",
    "Florian","Frank","Freek","Gianluca","Gijs","Hamid","Hans","Harm",
    "Hassan","Henk","Herman","Hugo","Ibrahim","Ivar","Jack","Jacco",
    "Jan","Jasper","Jeroen","Jesse","Jef","Joep","Johan","Johannes",
    "Joost","Jordan","Jos","Jouke","Jules","Julien","Karim","Kees",
    "Kevin","Kobe","Lander","Lars","Lasse","Lennart","Leon","Lorenzo",
    "Lowie","Luca","Lucas","Lukas","Maarten","Marc","Marcel","Marco",
    "Mario","Mark","Martijn","Martin","Mathijs","Matthias","Max",
    "Michael","Michiel","Milan","Mohamed","Nathan","Nick","Nico",
    "Niels","Noah","Noud","Oliver","Omar","Oscar","Pepijn","Peter",
    "Pieter","Pim","Quinten","Raf","Reinier","Remi","Ricardo","Rick",
    "Robin","Robbert","Robert","Ruben","Sam","Sander","Sebastian",
    "Sergio","Simon","Stefan","Stef","Steven","Stijn","Tibo","Timon",
    "Thijs","Thomas","Tijs","Tim","Tomas","Tom","Victor","Vincent",
    "Warre","Wim","Wouter","Wout","Xavier","Xander","Yannick","Yorick",
    "Zeno",
    # Vrouwelijk
    "Amber","Amelie","Amy","An","Anna","Anne","Anouk","Axelle","Babette",
    "Bieke","Bo","Charlotte","Chiara","Claire","Demi","Elena","Elien",
    "Elisa","Elisabeth","Elke","Eline","Ellen","Emma","Esther","Eva",
    "Fatima","Fien","Fiona","Floor","Flore","Hailey","Hanne","Helena",
    "Imke","Ines","Inge","Iris","Jana","Jasmine","Jolien","Julie",
    "Karen","Katja","Katrien","Kirsten","Laura","Layla","Lena","Lies",
    "Lien","Linde","Lisa","Loes","Lore","Lotte","Louise","Luna","Manon",
    "Maren","Maria","Marieke","Marina","Marjan","Maud","Merel","Mia",
    "Miriam","Nathalie","Nina","Noor","Nora","Olivia","Pauline","Petra",
    "Roos","Sara","Sarah","Silke","Simone","Sofia","Sofie","Sophie",
    "Stien","Tineke","Tinne","Tine","Trees","Valerie","Vera","Vicky",
    "Yasmin","Yasmine","Yara","Yvonne","Zoe",
}}

# Woorden die mid-zin met hoofdletter kunnen voorkomen maar geen naam zijn
NL_STOPWORDS: set[str] = {
    "de","het","een","en","in","van","op","te","dat","die","voor","met",
    "als","maar","ook","aan","er","nu","al","zo","bij","nog","dan","wel",
    "wat","naar","om","uit","door","over","tot","na","per","via","wordt",
    "zijn","hebben","kan","zal","mag","moet","zou","niet","meer","geen",
    "dit","andere","morgen","gisteren","vandaag",
    "maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag","zondag",
    "januari","februari","maart","april","mei","juni","juli","augustus",
    "september","oktober","november","december",
    "nederland","belgie","amsterdam","rotterdam","utrecht","eindhoven",
    "groningen","tilburg","breda","nijmegen","haarlem","arnhem",
    "blueprint","excel","word","teams","outlook","sharepoint","salesforce",
    "hubspot","microsoft","google","apple","linkedin","whatsapp","zoom","slack",
    "pii","ik","je","we","ze","hij","zij","u","jullie","hun","hen",
    "mij","jou","hem","haar","ons","omdat","zodat","wanneer","terwijl",
    "hoewel","indien","tenzij","zodra","volgens","echter","dus","want",
    "namelijk","immers","test","module","werkt","nummer","rekening",
    "deep","dive","dives","macbook",
}

# NER-labels → code-prefix
ENTITY_PREFIXES = {
    "PER":  "PERSOON",
    "ORG":  "BEDRIJF",
    "LOC":  "LOCATIE",
    "GPE":  "LOCATIE",
    "MISC": "OVERIG",
}

# Regex-patronen
REGEX_PATTERNS = [
    (r"€\s?\d[\d.,]*\s?(k|K|m|M|miljoen|duizend)?", "BEDRAG"),
    (r"\b\d[\d.,]*\s?(miljoen|duizend)\b",           "BEDRAG"),
    (r"\b\d[\d.,]*\s?%",                              "PERCENTAGE"),
    (r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", "EMAIL"),
    (r"\b(\+31|0)[1-9]\d{7,9}\b",                    "TELEFOON"),
    (r"\bNL\d{2}[A-Z]{4}\d{10}\b",                   "IBAN"),
    (r"\b\d{8,}\b",                                   "REKENING"),
]


def load_nlp():
    try:
        return spacy.load("nl_core_news_lg")
    except OSError:
        print("Fout: nl_core_news_lg niet gevonden.")
        print("  ~/whisper/venv/bin/python3 -m spacy download nl_core_news_lg")
        sys.exit(1)


def overlaps(start: int, end: int, spans: list[tuple[int, int]]) -> bool:
    return any(s < end and start < e for s, e in spans)


def collect_spans(text: str) -> list[tuple[int, int, str, str]]:
    """
    Verzamel alle te-vervangen spans uit de originele tekst.
    Retourneert: [(start, end, prefix, original_text), ...]
    Overlappende spans worden overgeslagen (eerste/langste wint).
    """
    nlp = load_nlp()
    candidates: list[tuple[int, int, str, str]] = []
    taken: list[tuple[int, int]] = []

    def add(start: int, end: int, prefix: str, original: str) -> None:
        if not overlaps(start, end, taken):
            candidates.append((start, end, prefix, original))
            taken.append((start, end))

    # Laag 1: regex (vóóraan zodat nummers niet als namen worden herkend)
    for pattern, prefix in REGEX_PATTERNS:
        for m in re.finditer(pattern, text):
            add(m.start(), m.end(), prefix, m.group(0))

    # Laag 2: spaCy NER — op ORIGINELE tekst, geen placeholders
    doc = nlp(text)
    for ent in sorted(doc.ents, key=lambda e: -(e.end_char - e.start_char)):
        prefix = ENTITY_PREFIXES.get(ent.label_)
        if not prefix or len(ent.text.strip()) <= 1:
            continue
        add(ent.start_char, ent.end_char, prefix, ent.text)

    # Laag 3a: voornamenlijst — op ORIGINELE tekst
    for name in sorted(DUTCH_FIRST_NAMES, key=len, reverse=True):
        for m in re.finditer(r"\b" + re.escape(name) + r"\b", text, re.IGNORECASE):
            add(m.start(), m.end(), "PERSOON", m.group(0))

    # Laag 3b: hoofdletter-heuristiek — mid-zin woorden die NER/lijst miste
    for m in re.finditer(r"\b([A-Z][a-záéíóúàèìòùëïü]{1,})\b", text):
        word = m.group(0)
        if word.lower() in NL_STOPWORDS:
            continue
        # Sla over als dit het eerste woord van een zin is
        before = text[:m.start()].rstrip(" \t")
        if not before or before[-1] in ".!?\n":
            continue
        add(m.start(), m.end(), "PERSOON", word)

    return candidates


def strip(text: str, existing_map: dict | None = None) -> tuple[str, dict]:
    mapping: dict = existing_map.copy() if existing_map else {}
    inverse: dict = {v.lower(): k for k, v in mapping.items()}
    counters: dict = {}

    for code in mapping.keys():
        parts = code.rsplit("_", 1)
        if len(parts) == 2 and parts[1].isdigit():
            prefix = parts[0]
            counters[prefix] = max(counters.get(prefix, 0), int(parts[1]))

    def assign_code(prefix: str, original: str) -> str:
        key = original.lower().strip()
        if key in inverse:
            return inverse[key]
        counters[prefix] = counters.get(prefix, 0) + 1
        code = f"{prefix}_{counters[prefix]:02d}"
        mapping[code] = original
        inverse[key] = code
        return code

    spans = collect_spans(text)

    # Vervang van achter naar voren zodat posities geldig blijven
    result = text
    for start, end, prefix, original in sorted(spans, key=lambda x: x[0], reverse=True):
        code = assign_code(prefix, original)
        result = result[:start] + code + result[end:]

    return result, mapping


def restore(text: str, mapping: dict) -> str:
    result = text
    for code, original in sorted(mapping.items(), key=lambda x: -len(x[0])):
        result = result.replace(code, original)
    return result


def print_mapping_table(mapping: dict) -> None:
    if not mapping:
        print("  (geen PII gevonden)")
        return
    max_code = max(len(k) for k in mapping)
    for code, original in sorted(mapping.items()):
        print(f"  {code:<{max_code}}  →  {original}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("mode", choices=["strip", "restore"])
    parser.add_argument("input", help="Invoerbestand (.txt)")
    parser.add_argument("--map", help="Pad naar mapping.json")
    parser.add_argument("--out", help="Uitvoerbestand")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Fout: bestand '{input_path}' niet gevonden.")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")

    if args.mode == "strip":
        map_path = Path(args.map) if args.map else input_path.with_suffix(".map.json")
        existing_map = json.loads(map_path.read_text()) if map_path.exists() else None
        out_path = (
            Path(args.out) if args.out
            else input_path.with_name(input_path.stem + "_anon.txt")
        )

        print(f"[pii_strip] Anonimiseren: {input_path.name}")
        anon_text, mapping = strip(text, existing_map)

        out_path.write_text(anon_text, encoding="utf-8")
        map_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2))

        print("[pii_strip] Gevonden en vervangen:")
        print_mapping_table(mapping)
        print(f"\n  Geanonimiseerd transcript : {out_path}")
        print(f"  Sleuteltabel (BEWAAR DIT) : {map_path}")

    elif args.mode == "restore":
        if not args.map:
            print("Fout: --map is verplicht bij restore.")
            sys.exit(1)
        map_path = Path(args.map)
        if not map_path.exists():
            print(f"Fout: mapping '{map_path}' niet gevonden.")
            sys.exit(1)
        out_path = (
            Path(args.out) if args.out
            else input_path.with_name(input_path.stem + "_restored.txt")
        )

        mapping = json.loads(map_path.read_text())
        print(f"[pii_strip] Terugzetten: {input_path.name} (mapping: {map_path.name})")
        restored = restore(text, mapping)
        out_path.write_text(restored, encoding="utf-8")
        print(f"  Hersteld bestand: {out_path}")


if __name__ == "__main__":
    main()
