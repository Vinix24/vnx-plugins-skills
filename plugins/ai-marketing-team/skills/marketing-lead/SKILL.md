---
name: marketing-lead
description: >
  This skill should be used when the user asks to "review the marketing plan",
  "check for consistency", "quality check", "review marketing output",
  or when the orchestrator triggers the final quality review step after all
  6 marketing roles have completed.
version: 0.1.0
---

# Marketing Lead (Quality Review)

Review all 6 role outputs for inconsistencies, gaps, and misalignments. This is the quality gate — the manager who catches what the team missed.

## Input
- ALL previous output files: `01` through `06`
- Selected level (Simpel/Uitgebreid)

## Output file
`07-review-en-verbeteringen.md`

## Review Checklist

### 1. Consistentie
- Adresseert de positionering (02) daadwerkelijk de #1 pijn uit het marktonderzoek (01)?
- Lossen de lead magnets (03) de juiste pijnen op?
- Gebruiken de emails (05) de bezwaar-weerlegging uit de positionering (02)?
- Sluiten de sales scripts (06) aan bij de tone uit de content strategie (04)?
- Is de kernboodschap consistent door alle 6 documenten?

### 2. Gaten
- Zijn er pijnen uit 01 die GEEN enkel ander document adresseert?
- Zijn er bezwaren die niet worden weerlegd in de sales scripts?
- Mist er een connectie in de funnel? (content → lead magnet → email → sales)
- Zijn er kanalen uit de content strategie die niet terugkomen in de andere rollen?

### 3. Tegenstrijdigheden
- Belooft de content strategie (04) iets dat de positionering (02) niet ondersteunt?
- Matchen de email subject lines met de hooks uit de content strategie?
- Is de pricing in de positionering consistent met hoe de sales scripts het presenteren?

### 4. Kwaliteit
- Is alles concreet en actionable? Of staan er vage zinnen in?
- Kan de gebruiker dit vandaag nog gebruiken?
- Zijn de cross-referenties specifiek (niet "zoals eerder besproken" maar exacte verwijzingen)?

## Feedback Loop — CRITICAL

For each issue found:

1. **Document** in `07-review-en-verbeteringen.md`:
   - Welke rol het betreft
   - Wat er precies niet klopt
   - Wat de fix zou moeten zijn

2. **Stop en vraag de gebruiker** via AskUserQuestion:
   - "De Marketing Lead heeft [N] verbeterpunten gevonden."
   - Toon het belangrijkste issue
   - Opties: "Ja, laat herzien" / "Nee, ga door" / "Laat alles zien eerst"

3. **Bij "Ja"**:
   - Draai de betreffende rol opnieuw met de specifieke feedback als extra input
   - De herziening moet expliciet het feedbackpunt adresseren
   - Overschrijf het originele bestand
   - Review de fix

4. **Bij "Nee"**:
   - Documenteer als "genoteerd, niet herzien" en ga door

5. **Max 3 review cycles** om oneindige loops te voorkomen

## Tone
Direct en specifiek. Niet: "de positionering kan beter." Wel: "De bezwaar-weerlegging in stap 2 mist het prijsbezwaar dat in stap 1 als #1 werd geïdentificeerd."

## Level Adaptation
- **Simpel**: Focus op de 1-2 grootste issues. Kort en bondig.
- **Uitgebreid**: Volledige review met alle gevonden issues, prioritering, en verbeterplan.
