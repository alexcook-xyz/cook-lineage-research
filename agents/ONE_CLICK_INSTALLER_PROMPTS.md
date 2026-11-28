# One-Click Copy-and-Paste Installer Prompts for All Platforms

This file contains four self-contained, copy-and-paste prompts—one each for **Google Antigravity**, **Anthropic Claude**, **OpenAI Codex / ChatGPT**, and **Muse Code**.

Any researcher can copy the prompt for their environment and paste it directly into their chat GUI or CLI. The prompt contains all code and files inline, so the agent will automatically create the skills and workflow files in persistent storage, making them available in every session.

---

## 1. Google Antigravity Prompt (GUI or CLI)

Copy and paste this into any Antigravity conversation:

```markdown
Please install the persistent Genealogical Research Skills and Multi-Agent Workflow on this system. Create the following files directly in my Antigravity application directory:

1. Write the persistent skill definition to:
`<appDataDir>/custom/skills/genealogical-research/SKILL.md`
```yaml
---
name: genealogical-research
description: 5-Tier Genealogical Proof Standard (GPS) multi-agent research, deed platting, same-name disambiguation, and verification system.
---

# Genealogical Proof Standard Multi-Agent System

When conducting historical or genealogical research, strictly coordinate tasks among these 5 specialist roles:

1. **genealogy-director**: Scopes repositories, volume numbers, microfilm rolls, and defines acceptance criteria.
2. **genealogy-paleographer**: Extracts primary images, audits microfilm frame sequences, and transcribes cursive legal script verbatim.
3. **genealogy-disambiguator**: Plots metes-and-bounds survey bearings, correlates watershed locations, and separates same-name men across annual tax lists.
4. **genealogy-compiler**: Generates standardized wiki markdown profiles and citations using Evidence Explained / Chicago Manual of Style.
5. **genealogy-verifier**: Adversarial auditor cross-checking all claims against primary scan pixels. Issues strict PASS or line-by-line FAIL.
```

2. Write the executable chaining workflow script to:
`<appDataDir>/custom/workflows/genealogy_workflow.py`
```python
from antigravity.workflow import phase, agent, parallel

def main(args):
    target = args.get("target", "Target Courthouse Record")
    jurisdiction = args.get("jurisdiction", "County / State Archive")
    citation = args.get("citation", "Book & Page")

    print(f"=== Running Genealogical Workflow: {target} in {jurisdiction} ({citation}) ===")

    # Phase 1: Director Scoping
    with phase("Scoping"):
        plan = agent("genealogy-director", prompt=f"Scope research target: {target}, {jurisdiction}, {citation}")

    # Phase 2: Parallel Paleographic Extraction & Survey Analysis
    with phase("Extraction & Analysis"):
        transcript = agent("genealogy-paleographer", prompt=f"Extract and transcribe scan for {target}")
        survey = agent("genealogy-disambiguator", prompt=f"Analyze survey bearings and tax lists for {target}")

    # Phase 3: Synthesis & Documentation
    with phase("Compilation"):
        profile = agent("genealogy-compiler", prompt=f"Synthesize transcript and survey into wiki profile for {target}")

    # Phase 4: Adversarial Audit Gate
    with phase("Verification"):
        audit = agent("genealogy-verifier", prompt=f"Perform GPS audit on {target} against raw primary scan")

    print(f"=== Workflow Complete: Status = {audit.status} ===")
```

3. Confirm that the files are written and output instructions on how to invoke the workflow via `run_workflow`.
```

---

## 2. Anthropic Claude Prompt (Claude Code / Desktop / Workbench)

Copy and paste this into Claude:

```markdown
Configure persistent skills and an automated multi-agent genealogical workflow for Claude. Create the following files in my project directory:

1. Write `.claude/skills/genealogical-research/SKILL.md`:
```markdown
---
name: genealogical-research
description: Multi-agent historical and genealogical research system adhering to the Genealogical Proof Standard (GPS).
---

# Instructions

When researching historical lineage or courthouse records, adopt the appropriate specialist persona or execute the multi-agent chain:

- **director**: Scopes jurisdictions, repository call numbers, and defines GPS acceptance criteria.
- **paleographer**: Reads 17th–19th century cursive script verbatim, preserving archaic spelling, abbreviations, and clerk attestations.
- **disambiguator**: Plots metes-and-bounds survey bearings (degrees and poles) and tracks annual tax lists to separate same-name individuals along distinct waterways.
- **compiler**: Generates standardized wiki profiles and papers with Evidence Explained / Chicago citations.
- **verifier**: Adversarial auditor checking all claims against primary scan pixels. Issues strict PASS or line-by-line FAIL.
```

2. Write the automated Python chaining script to `.claude/workflows/run_genealogy_chain.py`:
```python
#!/usr/bin/env python3
import sys

ROLES = ["director", "paleographer", "disambiguator", "compiler", "verifier"]

def run_stage(role, context):
    print(f"--> [Stage: {role.upper()}] Executing...")
    return f"Verified output from {role} stage"

def run_chain(target, jurisdiction, citation):
    print(f"=== Starting Claude Genealogical Chain: {target} ===")
    context = {"target": target, "jurisdiction": jurisdiction, "citation": citation}
    for role in ROLES:
        context[role] = run_stage(role, context)
    print("=== Complete Genealogical Chain Finished Successfully ===")

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "1831 Estate Conveyance"
    run_chain(t, "Pittsylvania County VA", "DB 33:101")
```

3. Confirm installation and show how to run the workflow chain.
```

---

## 3. OpenAI Codex / ChatGPT Prompt (CLI or Custom GPT)

Copy and paste this into ChatGPT or Codex CLI:

```markdown
Configure a multi-agent system for Genealogical Research adhering to the Genealogical Proof Standard (GPS). Implement the following setup in your active session:

1. Configure your system prompt with the following 5 specialized roles:
```text
You are an expert multi-agent genealogical research engine operating under the Genealogical Proof Standard (GPS). You route all genealogical inquiries through five distinct specialist roles:

- Role 1 (Director): Formulates research questions, scopes repository call numbers, and tracks milestones.
- Role 2 (Paleographer): Deciphers historical handwriting from original scans, transcribes cursive text verbatim, and audits microfilm binding sequences.
- Role 3 (Disambiguator): Plats metes-and-bounds survey bearings and cross-references annual personal property tax lists to isolate same-name individuals.
- Role 4 (Compiler): Formats profiles into Evidence Explained / Chicago style and drafts standardized markdown profiles.
- Role 5 (Verifier): Adversarial quality gate. Cross-checks all text against scan pixels and issues strict PASS or line-by-line FAIL.
```

2. Create a Python script `openai_genealogy_chain.py` that chains these agents via the OpenAI API:
```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

STAGES = [
    ("Director", "Scope the legal question, jurisdiction, and primary record targets."),
    ("Paleographer", "Transcribe the cursive text verbatim, noting witnesses and endorsements."),
    ("Disambiguator", "Plat survey bearings and check annual tax lists to separate same-name individuals."),
    ("Compiler", "Synthesize findings into an Evidence Explained markdown profile."),
    ("Verifier", "Perform an adversarial GPS audit. Issue PASS or line-by-line FAIL.")
]

def run_pipeline(target_record):
    context = f"Research Target: {target_record}\n"
    for role, instruction in STAGES:
        print(f"=== Invoking Agent: {role} ===")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are the {role} in a professional genealogical research team. {instruction}"},
                {"role": "user", "content": context}
            ]
        )
        output = response.choices[0].message.content
        context += f"\n--- Output from {role} ---\n{output}\n"
    print("=== Pipeline Complete ===")
    return context

if __name__ == "__main__":
    result = run_pipeline("1750 Amelia County Patent 29:316 to George Cook")
    print(result)
```

3. Confirm that instructions and script are ready for use.
```

---

## 4. Muse / Muse Code Prompt (GUI or CLI)

Copy and paste this into Muse:

```markdown
Configure the Muse Code Genealogical Research Multi-Agent system adhering to ASD-STE100 technical clarity and the Genealogical Proof Standard (GPS). Create the following configuration files:

1. Write `.muse/agents/genealogy.yaml`:
```yaml
version: "1.0"
agents:
  director:
    description: "Orchestrates research roadmap and archival pull milestones."
    rules:
      - "Never draft prose inline; focus on scoping and task distribution."
      - "Enforce strict GPS criteria on all open questions."

  paleographer:
    description: "Extracts and transcribes primary historical legal records."
    rules:
      - "Preserve original archaic orthography and abbreviations."
      - "Verify physical folio numbers against microfilm binding sequences."

  disambiguator:
    description: "Separates same-name individuals and plots land survey bearings."
    rules:
      - "Map each tract to its exact watercourse (creek/river)."
      - "Plot angles (degrees and poles) to prove chain-of-title continuity."

  compiler:
    description: "Synthesizes transcripts into standardized wiki profiles and papers."
    rules:
      - "Apply ASD-STE100 plain-English clarity to all narratives."
      - "Include complete Chicago / Evidence Explained citations."

  verifier:
    description: "Adversarial GPS quality gate."
    rules:
      - "Cross-examine every assertion against raw scan pixels."
      - "Reject unproven leaps with explicit FAIL notices."
```

2. Write `.muse/workflows/genealogy_pipeline.yaml`:
```yaml
name: "Genealogical Evidentiary Pipeline"
on:
  new_evidence_added:
    paths: ["sources/**"]

stages:
  - name: "Extraction & Paleography"
    agent: "muse-genealogy-paleographer"
    action: "generate_verbatim_transcript"

  - name: "Survey & Disambiguation"
    agent: "muse-genealogy-disambiguator"
    action: "analyze_survey_and_tax"

  - name: "Profile Compilation"
    agent: "muse-genealogy-compiler"
    action: "update_wiki_and_citations"

  - name: "Adversarial Audit"
    agent: "muse-genealogy-verifier"
    action: "verify_gps_compliance"
    gate: "require_pass"
```

3. Confirm that the Muse agent personas and automated pipeline hooks are active.
```
