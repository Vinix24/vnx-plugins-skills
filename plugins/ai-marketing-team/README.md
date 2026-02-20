# AI Marketing Team

Build a complete AI marketing team in Claude Cowork — 6 specialized roles that work together as one marketing department.

## What it does

One command launches 6 marketing specialists that build on each other's work:

1. **Marktonderzoeker** — doelgroep, pijnen, kooptriggers
2. **Positioneringsexpert** — aanbod, pricing, bezwaren weerleggen
3. **Lead Magnet Specialist** — lead magnets gebaseerd op onderzoek
4. **Content Strateeg** — contentplan, hooks, retargeting
5. **E-mail Specialist** — email sequences die converteren
6. **Sales Copywriter** — belscripts en objection handling

Each role reads the output of all previous roles, creating an interconnected marketing plan — not 6 disconnected documents.

## Built-in Quality Check: Marketing Lead

After the 6 roles complete, a 7th step kicks in: the **Marketing Lead**. This role reviews all output for inconsistencies, gaps, and misalignments between roles.

The key difference: when the Marketing Lead finds an issue, it doesn't silently fix it. It stops and asks **you**:

> "De positionering in stap 2 sluit niet aan bij de pijnen uit stap 1. Wil je dat ik de Positioneringsexpert dit laat herzien?"

You decide. Say yes → that role reruns with specific feedback. Say no → move on.

This is how a real team works: a manager who catches problems, escalates when needed, and keeps you in control. Not an AI running in circles — but a quality loop with a human in the lead.

## Two Levels

- **Simpel** — for MKB-ondernemers who want a practical, ready-to-use plan
- **Uitgebreid** — for marketing professionals who want strategic depth

## Usage

Run `/marketing-team` and follow the prompts. You'll get 6 separate files, each building on the last.

## Output

Six markdown files saved to your workspace folder:

| File | Role |
|------|------|
| `01-marktonderzoek.md` | Market research & audience analysis |
| `02-positionering.md` | Positioning & value proposition |
| `03-lead-magnets.md` | Lead magnet concepts & landing page copy |
| `04-content-strategie.md` | Content plan & calendar |
| `05-email-sequences.md` | Email sequences (welcome, nurture, sales) |
| `06-sales-scripts.md` | Call scripts & objection handling |
| `07-review-en-verbeteringen.md` | Marketing Lead review & corrections |

## How it's different from "AI prompt sets"

Most "AI marketing teams" are 6 separate prompts that don't talk to each other. This plugin is different:

- **Sequentieel opgebouwd** — each role builds on all previous output, not in isolation
- **Cross-referencing** — the email specialist references specific pains from the market research, not generic advice
- **Quality loop** — the Marketing Lead catches inconsistencies and asks you to rerun roles when needed
- **You stay in control** — no AI running autonomously. You approve every correction.

## Author

Vincent van Deth — Builder-Coach | AI Marketing Strategy for B2B MKB
