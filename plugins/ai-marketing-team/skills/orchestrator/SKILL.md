---
name: orchestrator
description: >
  This skill should be used when the user asks to "build a marketing team",
  "create a marketing plan", "set up AI marketing agents", "run the marketing workflow",
  "generate a complete marketing strategy", or wants all marketing roles to work
  together on their business. Also triggers on "marketingteam", "marketing afdeling",
  or "complete marketingplan".
version: 0.1.0
---

# AI Marketing Team Orchestrator

Coordinate 7 specialized marketing roles that work as one team. This skill manages the sequence, passes context between roles, and triggers the quality review loop.

## Workflow

Execute the roles in this exact order. For each role, read its SKILL.md to get the detailed instructions.

| Step | Skill folder | Output file | Builds on |
|------|-------------|-------------|-----------|
| 1 | `marktonderzoeker` | `01-marktonderzoek.md` | User input |
| 2 | `positioneringsexpert` | `02-positionering.md` | Step 1 |
| 3 | `lead-magnet-specialist` | `03-lead-magnets.md` | Steps 1-2 |
| 4 | `content-strateeg` | `04-content-strategie.md` | Steps 1-3 |
| 5 | `email-specialist` | `05-email-sequences.md` | Steps 1-4 |
| 6 | `sales-copywriter` | `06-sales-scripts.md` | Steps 1-5 |
| 7 | `marketing-lead` | `07-review-en-verbeteringen.md` | Steps 1-6 |

## Level Selection

Before starting, ask the user which level they want using AskUserQuestion:

**Simpel** (MKB-ondernemer):
- Fewer questions, faster output
- Practical language, no jargon
- Ready-to-use deliverables

**Uitgebreid** (Marketing professional):
- Deeper analysis at each step
- More strategic options and trade-offs
- Metrics, KPIs, and benchmarks included

Pass the selected level to each role.

## Input Gathering

After level selection, gather these essentials:

1. **Bedrijf**: Naam, wat ze doen, sector
2. **Doelgroep**: Wie zijn de ideale klanten?
3. **Aanbod**: Wat verkopen ze? Prijsindicatie?
4. **Doel**: Wat willen ze bereiken? (meer leads, meer omzet, naamsbekendheid)
5. **Huidige situatie**: Wat doen ze nu aan marketing? (optioneel)

## Execution Rules

1. **Read each role's SKILL.md** before executing that role
2. **Pass all previous output files** as context to the next role
3. **Save each output** as a separate .md file in the workspace folder
4. **Language**: All output in Dutch
5. **Tone**: Practical, direct, no consultant-jargon
6. **Cross-references**: Each role must explicitly reference findings from previous roles
7. **Actionable**: Every deliverable must be usable TODAY

## Level Adaptations

Read `references/level-guide.md` for how each role adapts between Simple and Advanced modes.

## Completion

After all 7 roles are complete (including any reruns triggered by the Marketing Lead):
1. Provide a summary with links to all 7 files
2. Note which roles were rerun and why (if any)
3. Highlight the 3 most impactful quick wins
4. Suggest a recommended execution order ("start hier")
5. Ask if the user wants to dive deeper into any specific role
