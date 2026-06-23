---
name: transcribe
description: Lokale spraaktranscriptie op de eigen Mac (geen cloud, geen externe AI), met mlx-whisper en optioneel spreker-diarization (pyannote) en PII-strip. PII en diarization zijn onafhankelijk aan/uit te zetten, dus alle vier de combinaties zijn mogelijk. Gebruik bij "transcribeer", "transcriptie", "opname uitwerken", "gesprek/interview transcriberen", "maak een transcript", "zet deze .m4a/.wav om naar tekst", of wanneer een klant- of deep-dive-opname privacy-veilig en lokaal naar tekst moet. Werkt voor elk project of klantmap.
---

# Local Transcription

Volledig lokale spraaktranscriptie. De audio en de tekst verlaten de machine niet. Dit is de centrale, herbruikbare versie van de toolchain; gebruik deze voor elk project.

## Wanneer gebruiken

Een opname (`.m4a`, `.wav`, `.mp3`, ...) moet naar tekst, en het is gevoelig genoeg dat het lokaal moet blijven: klantgesprekken, stakeholder-interviews, deep dives, board-gesprekken. Geen Fireflies of andere cloud-transcriptie voor dit soort materiaal.

## Configureerbaar: PII en diarization los van elkaar

Twee onafhankelijke vlaggen, `-p` (PII-strip) en `-d` (diarization). Vier combinaties:

| Wens | Vlaggen | Output-bestanden |
|---|---|---|
| Vol transcript, namen erin | (geen) | `<out>.txt` |
| Met sprekers, namen erin | `-d` | `<out>.txt`, `<out>_diarized.txt` |
| Zonder klantdata, geen sprekers | `-p` | `<out>_anon.txt`, `<out>.map.json` |
| Zonder klantdata, mét sprekers | `-p -d` | bovenstaande + `<out>_diarized_anon.txt` |

De `.map.json` is de sleuteltabel (pseudoniem → echte waarde). Bij `-p -d` wordt de diarized-output met diezelfde sleuteltabel geanonimiseerd, zodat pseudoniemen consistent zijn over beide bestanden.

## Preflight (eenmalig per machine controleren)

```
ls ~/whisper/venv/bin/mlx_whisper && which ffmpeg && \
  ls ~/.cache/huggingface/hub/ | grep whisper-large-v3-turbo && \
  ~/whisper/venv/bin/python3 -c "import pyannote.audio; print('pyannote OK')"
```

Vier keer groen = klaar. Bevestigd aanwezig op de Mac Mini. Diarization gebruikt het gated pyannote-model (`pyannote/speaker-diarization-community-1`); de HuggingFace-login moet eenmalig gedaan zijn.

## Gebruik

Het script staat naast deze SKILL.md. Roep het aan met `bash`:

```bash
SKILL="$HOME/.claude/skills/transcribe"

# Vol transcript (namen erin, geen sprekers)
bash "$SKILL/transcribe.sh" -o uitvoer.txt opname.m4a

# Met sprekers (namen erin)
bash "$SKILL/transcribe.sh" -d -o uitvoer.txt opname.m4a

# Zonder klantdata (PII-stripped, geen sprekers)
bash "$SKILL/transcribe.sh" -p -o uitvoer.txt opname.m4a

# Zonder klantdata, mét sprekers
bash "$SKILL/transcribe.sh" -p -d -o uitvoer.txt opname.m4a

# Sprekerhint (bv. 1-op-1 = 2 sprekers) scherpt de diarization aan
bash "$SKILL/transcribe.sh" -p -d -n 2 -o uitvoer.txt opname.m4a
```

Flags: `-p` PII-strip, `-d` diarization, `-n` sprekerhint, `-o` uitvoerbestand, `-l taal|auto` taal (standaard `nl`), `-e cpp|mlx` engine (standaard mlx; diarization vereist mlx).

Taal: standaard `nl`. Bij meertalige opnames (bv. Nederlands + Engels + Frans door elkaar) `-l auto` voor autodetectie, of `-l en` / `-l fr` als één taal domineert. Whisper detecteert per bestand, niet per zin, dus bij sterk gemengde opnames is het soms beter per spreker/segment apart te draaien.

```bash
# Meertalige opname, laat de taal detecteren
bash "$SKILL/transcribe.sh" -d -l auto -o uitvoer.txt opname.m4a
```

## Werkwijze bij meerdere opnames

- Transcribeer kortste bestand eerst, zo zijn de eerste transcripts snel binnen.
- Lange opnames (>30 min) met diarization duren; draai ze op de achtergrond.
- Output van een klantmap hoort in de `transcripts/` map van die klant, niet in deze skill-map.

## Sprekers mappen

Diarization levert `SPREKER_00`, `SPREKER_01`, ... Map die naar echte namen op basis van de inhoud (de interviewer is doorgaans Vincent). Doe dit ná de transcriptie, met de inhoud erbij.

## Privacy-discipline

- Analyseer op de `_anon.txt` / `_diarized_anon.txt` als het materiaal gedeeld of buiten de eigen machine verwerkt wordt; bewaar de `.map.json` lokaal.
- Voor een eigen, lokale afdronk mogen de niet-geanonimiseerde bestanden, mits ze op de machine blijven.
- Wis de ruwe opname na verwerking als de klant-NDA dat vraagt.
- Vraag mondeling opname-akkoord vóór elk gesprek.

## Restore

Pseudoniemen terugzetten naar de echte waarden:

```bash
~/whisper/venv/bin/python3 "$SKILL/pii_strip.py" restore uitvoer_anon.txt --map uitvoer.map.json
```

## Bestanden in deze skill

- `transcribe.sh` — orchestratie (ffmpeg → mlx-whisper → optioneel diarize → optioneel PII-strip)
- `diarize_merge.py` — pyannote-diarization, plakt sprekerlabels op de Whisper-segmenten
- `pii_strip.py` — pseudonimisering (regex + spaCy NER + namenlijst), met herbruikbare sleuteltabel
