---
description: Start je AI Marketing Team — 7 rollen, één compleet marketingplan
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
argument-hint: "[bedrijfsnaam of product]"
---

# AI Marketing Team

Launch the full AI Marketing Team workflow.

Read the `orchestrator` skill to coordinate all 7 marketing roles. The orchestrator manages the sequence, passes context between roles, and triggers the quality review loop.

Each role has its own skill with detailed instructions. Read each role's SKILL.md before executing that role.

The workflow:
1. Ask the user for their level (Simpel/Uitgebreid)
2. Gather business input
3. Execute roles 1-6 in order, saving each output file
4. Run the Marketing Lead (role 7) quality review
5. Handle feedback loops if issues are found
6. Deliver summary with links to all files

All output in Dutch. Practical, actionable, no consultant-jargon.
