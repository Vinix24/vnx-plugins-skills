# Je eigen landingspagina

Een kant-en-klaar website-geraamte. Vul het met je eigen tekst en kleuren, open het, en zet het online.

## Geen techneut? In drie stappen

1. Download deze map (de groene knop "Code", dan "Download ZIP").
2. Dubbelklik op `index.html`. Je ziet de pagina meteen in je browser.
3. Wil je hem op maat? Plak de prompt hieronder, samen met de inhoud van `index.html`, in ChatGPT, Claude of Gemini. Plak het antwoord terug in `index.html` en sla op.

### De vul-prompt (kopieer en plak)

```
Hier is een HTML-landingspagina met placeholder-teksten tussen rechte haken.
Vul hem voor mijn bedrijf: [naam], wij doen [wat je doet] voor [voor wie].
- Vervang alle placeholders door echte, wervende Nederlandse teksten.
- Pas de kleuren aan naar [jouw stijl of kleuren] door alleen de waarden onder :root te wijzigen.
- Verander verder niets aan de structuur.
Geef de volledige aangepaste index.html terug.

[plak hier de volledige inhoud van index.html]
```

## Wel handig?

- **Kleuren** pas je op één plek aan: de variabelen onder `:root` boven in `index.html` (`--brand`, `--accent`, enzovoort).
- **Je logo**: vervang de tekst in `<div class="logo">` door `<img src="logo.png" alt="[BEDRIJFSNAAM]" height="40">` en zet je logo-bestand ernaast.
- **Online zetten**: sleep de map naar [netlify.com/drop](https://app.netlify.com/drop), of importeer de repo in [vercel.com](https://vercel.com). In een paar klikken live.

Het geraamte werkt volledig offline: geen externe scripts, geen tracking, niks dat de cloud in gaat tot jij het online zet.
