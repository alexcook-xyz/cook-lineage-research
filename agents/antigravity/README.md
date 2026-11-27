# Antigravity Multi-Agent Skills & Workflow Installer

This installer configures the 5 standardized genealogical research roles as **persistent skills** and installs an automated multi-agent workflow script in Google Antigravity. Once installed, these skills are available automatically in every Antigravity session.

---

## One-Click Copy-and-Paste Installer Prompt

Copy and paste the prompt below directly into your Antigravity chat window:

```markdown
Install the standardized Genealogical Research Multi-Agent system for Antigravity. Perform the following steps:

1. Create persistent skill directory:
   `<appDataDir>/custom/skills/genealogical-research/`
   containing `SKILL.md` defining the 5 specialized agent subagents:
   - `genealogy-director`: Orchestrates roadmap milestones, scopes specific archive/film questions, and coordinates deliverables.
   - `genealogy-paleographer`: Retrieves courthouse scans, crops high-DPI plates, checks microfilm offsets, and transcribes cursive legal script verbatim.
   - `genealogy-disambiguator`: Plots metes-and-bounds survey bearings, tracks annual personal property and land tax lists, and isolates same-name individuals by watercourse.
   - `genealogy-compiler`: Compiles wiki profiles, research papers, and formats citations in full Chicago / Evidence Explained style.
   - `genealogy-verifier`: Adversarial GPS quality auditor cross-checking all drafted claims against primary image pixels with strict PASS/FAIL gates.

2. Create workflow script:
   `<appDataDir>/custom/workflows/genealogy_workflow.py`
   executable via `run_workflow`. The script must accept arguments `{target, jurisdiction, citation, phase}` and chain:
   - `phase('scoping')`: Invokes `genealogy-director`.
   - `phase('extraction')`: Invokes `genealogy-paleographer` to produce verbatim transcripts and plate crops.
   - `phase('analysis')`: Invokes `genealogy-disambiguator` to verify survey bearings and tax list continuity.
   - `phase('synthesis')`: Invokes `genealogy-compiler` to draft the wiki profile and citations.
   - `phase('audit')`: Invokes `genealogy-verifier` to inspect images and issue formal verification sign-off.

3. Verify installation and confirm when ready to execute on any county courthouse or colonial record target.
```

---

## Persistent Skill Implementation (`SKILL.md`)

```yaml
---
name: genealogical-research
description: Professional multi-agent genealogical research, deed platting, same-name disambiguation, and GPS verification system.
---

# Genealogical Research Standard Operating Procedures

When conducting historical or genealogical research, adhere strictly to the 5-Tier division of labor:

## Agent Definitions & Roles
1. **Director (`genealogy-director`):** Scopes the research goal, opens issues, and defines acceptance criteria.
2. **Paleographer (`genealogy-paleographer`):** Extracts digital images, checks folio numbers against binding sequences, and transcribes cursive text verbatim.
3. **Disambiguator (`genealogy-disambiguator`):** Plots survey bearings, checks tithable tax lists, and correlates neighbor clusters (FAN Club).
4. **Compiler (`genealogy-compiler`):** Drafts wiki person profiles, formats *Evidence Explained* footnotes, and updates lineage tables.
5. **Verifier (`genealogy-verifier`):** Inspects raw scan pixels, checks negative sweeps, and signs off with PASS or line-by-line FAIL.
```

---

## Multi-Agent Workflow Script (`genealogy_workflow.py`)

Run this workflow directly from Antigravity with `run_workflow`:

```python
# C:\Users\alx93781\.gemini\antigravity-cli\custom\workflows\genealogy_workflow.py
from antigravity.workflow import phase, agent, parallel

def main(args):
    target = args.get("target", "Target Record")
    jurisdiction = args.get("jurisdiction", "County Courthouse")
    citation = args.get("citation", "Book & Page")

    print(f"=== Starting Genealogical Workflow: {target} in {jurisdiction} ===")

    # Phase 1: Director Scoping
    with phase("Scoping"):
        plan = agent("genealogy-director", prompt=f"Scope research target: {target}, {jurisdiction}, {citation}")

    # Phase 2: Paleographic Extraction & Survey Analysis in Parallel
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
