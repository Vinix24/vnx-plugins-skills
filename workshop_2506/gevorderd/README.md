# Voor de gevorderden

Heb je al ervaring met AI-tools of automatiseringen (n8n, Make), dan kun je een stap verder dan een Gem of een losse prompt. Drie richtingen.

## 1. Je prompt als skill, niet als losse tekst

De prompts in `../assistent/prompts.md` werken in elke chatbot. Wil je ze permanent, leg ze dan vast:
- **Gemini:** maak een Gem en plak de prompt bij de instructies. Gratis, deelbaar via een link.
- **ChatGPT:** maak er een custom GPT of een Project van (vereist een betaald account).
- **Claude:** maak een Project en zet de prompt bij de instructies, of bouw een echte Claude-skill.

## 2. Automatisering: van no-code naar je eigen server

- **Make.com / Zapier:** no-code, snel te starten, gehost door hen, je betaalt per actie.
- **n8n:** ook visueel, maar open source. Je kunt het op je **eigen server** draaien, dan blijft je data bij jou, en je kunt er code in zetten als je verder wilt. De stap van no-code naar code.

Een eigen n8n-server plus een lokaal model betekent dat zowel de automatisering als de AI op je eigen machine draait. Dan gaat er niets de cloud in.

## 3. Lokaal transcriberen met namen eruit (de transcribe-skill)

In `transcribe/` staat een kant-en-klare Claude Code-skill: spraak naar tekst, volledig lokaal (mlx-whisper), met optioneel spreker-herkenning en een PII-strip die namen en bedrijven vervangt. Niets gaat de cloud in.

Installeren: kopieer de map `transcribe/` naar `~/.claude/skills/transcribe/`. Vereist Claude Code plus mlx-whisper op een Mac (Apple Silicon). Daarna vraag je Claude Code gewoon "transcribeer deze opname en strip de namen".

Dit is de skill-versie (werkt in Claude Code). Wil je hetzelfde in Claude Desktop of Codex, dan wrap je dezelfde scripts als een MCP-server.

## 4. MCP: de koppeling tussen je AI en je programma's

MCP (Model Context Protocol) is de standaardstekker waarmee een AI-agent veilig op je systemen aansluit: mail, agenda, boekhouding, bestanden. Het is vendor-neutraal en er zijn duizenden publieke MCP-servers.

Wil je hiermee aan de slag, dan is dat een echt project (een MCP-server opzetten en koppelen aan een agent zoals Claude of Codex). Dat valt buiten deze repo, maar het is de logische volgende stap als je je eigen tools aan een agent wilt hangen. Vraag het me gerust.

## 5. Agents: AI die zelf stappen zet

Een prompt antwoordt één keer. Een workflow loopt vaste stappen af. Een agent beslist zelf welke stappen nodig zijn, gebruikt je tools, en stopt of vraagt je iets als hij vastloopt.

Stel je een offerte-agent voor, voortbouwend op de offerte-naar-JSON uit de bibliotheek:

1. Ziet een nieuwe offerte binnenkomen in een map of mailbox.
2. Leest hem uit naar een vast format.
3. Controleert de sommen met een vaste regel (telt op, checkt de BTW).
4. Klopt alles? Direct je systeem in. Mist een prijs of klopt een totaal niet? Hij stopt en legt het aan jou voor.

Dat laatste is de kern: de agent doet het saaie werk, jij beslist alleen nog over de uitzonderingen. Geen stapel PDF's meer overtypen, en toch grip, omdat de laatste check menselijk blijft.

Dit is precies het soort systeem dat ik voor bedrijven bouw: een agent op één terugkerende, tijdrovende klus, met vaste regels eromheen en een menselijke eindcontrole. Meetbaar, en als het moet volledig op je eigen machine zodat je data binnen blijft.

Eerlijke verwachting: op vrije, open taken slagen agents nog lang niet altijd. De winst zit in begrensde, herhaalbare klussen, niet in onbewaakte betalingen. Daar zit ook het vak: de grenzen goed zetten.

Benieuwd wat dit voor jouw offertes, mail of documenten zou schelen? advies@vincentvandeth.nl

---

Vragen over deze hoek? advies@vincentvandeth.nl
