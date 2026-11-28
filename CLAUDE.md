# Genealogy Research Repository

This repository follows the Genealogical Proof Standard (GPS) and the conventions in
https://github.com/alexcook-xyz/genealogy-agent-skills/blob/main/CONVENTIONS.md.
The `genealogy` Claude Code plugin supplies the agents and skills.

## Non-negotiable rules
- No fact without a `[[S-...]]` source. Inference is labeled as inference.
- Record every search in `questions/Q-n/log.md`, including searches that found nothing.
- Never merge two people without an identity argument (skill: `person-dedupe`).
- Online trees, compiled pedigrees, and AI output are leads, never evidence.
- `confidence: proven` requires `questions/Q-n/proof.md` and a `review.md` with `verdict: pass`
  written by the `adversarial-reviewer` agent.
- When evidence runs out, stop and mark the question `stalled`. Do not fill the gap.
- Living people: no details in public places. No DNA match names or kit numbers in any file.

## Workflow
One GitHub issue per research question → `/gps-research-question <issue>` →
one branch and one PR per question → `python3 tools/validate.py .` must pass.

## Reusable knowledge
Anything learned that would help *other* questions (archive quirks, record coverage,
jurisdiction changes, search tricks) goes to the skills repo via the `knowledge-capture` skill.
Facts about specific people stay here.
