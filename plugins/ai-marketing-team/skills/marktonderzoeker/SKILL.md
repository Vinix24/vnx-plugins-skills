---
name: marktonderzoeker
description: >
  This skill should be used when the user asks for "marktonderzoek", "doelgroepanalyse",
  "target audience research", "kooptriggers", "klantpijnen", or wants to understand
  their ideal customer profile, buying triggers, and market dynamics.
version: 0.1.0
---

# Marktonderzoeker

Research the target market and build a complete picture of the ideal customer.

## Input
- Business info provided by the user (or from orchestrator)
- Selected level (Simpel/Uitgebreid)

## Output file
`01-marktonderzoek.md`

## Deliverables

### Doelgroepprofiel
- Demographics (leeftijd, functie, bedrijfsgrootte, sector)
- Online gedrag (waar ze content consumeren, welke platforms)
- Beslissingsproces (wie beslist, hoe lang duurt het, wie beïnvloedt)

### Pijnen en Frustraties
- Identificeer de belangrijkste pijnen met onderbouwing
- Rangschik op impact (welke pijn kost het meest?)
- Beschrijf hoe de pijn zich uit in dagelijks werk

### Behoeften en Wensen
- Wat willen ze bereiken? (outcomes, niet features)
- Wat is de droom-situatie?
- Verschil tussen wat ze zeggen te willen en wat ze echt nodig hebben

### Kooptriggers
- Welke events of momenten zetten hen aan tot actie?
- Seizoensgebonden triggers?
- Pain threshold: wanneer wordt het urgent genoeg om te handelen?

### Kanalen en Communities
- Waar bevinden ze zich online?
- Welke events/conferenties bezoeken ze?
- Wie volgen ze / wie beïnvloedt hen?

### Verwachte Bezwaren
- Lijst van redenen waarom ze NIET zouden kopen
- Rangschik van meest naar minst voorkomend
- Noteer de onderliggende angst achter elk bezwaar

## Tone
Write as a researcher presenting findings — factual, specific, evidence-based. No vague claims. If something is an aanname, label it as such.

## Cross-reference rule
This is the first role — there are no previous outputs. But flag any areas where you need more info from the user before the next roles can do their werk.
