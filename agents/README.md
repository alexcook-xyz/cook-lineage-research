# Multi-Agent Genealogical Research & Workflow Prompts

This directory provides ready-to-use, copy-and-paste installer prompts that configure the standardized 5-tier genealogical research agents and their automated chaining workflows across four major LLM / agentic platforms:

1. **[Antigravity (Google DeepMind CLI & IDE)](antigravity/README.md)** — Configures native persistent skills (`.gemini/antigravity-cli/custom/skills/`) and dynamic multi-agent workflow scripts using `run_workflow` / `invoke_subagent`.
2. **[Claude (Anthropic Claude Code / Workbench / Desktop)](claude/README.md)** — Configures persistent Claude Code skills, subagent definitions, and workflow chains via `.claude/skills/` and system instructions.
3. **[Codex / OpenAI (ChatGPT Advanced / Custom GPTs / Codex CLI)](codex/README.md)** — Configures OpenAI custom GPT instructions, function-calling agent tools, and multi-agent chaining prompts.
4. **[Muse / Muse Code](muse/README.md)** — Configures Muse-native agent configurations, review hooks, and ASD-STE100 / GPS evidentiary review pipelines.

---

## The 5 Standardized Genealogical Roles

Regardless of the LLM platform chosen, each installer sets up the exact same 5 specialized research roles:

| Tier | Role Name | Core Mandate |
|:---:|---|---|
| **Tier 1** | **`genealogy-director`** | Session orchestration, roadmap milestones, issue assignment, and coordinator oversight. |
| **Tier 2** | **`genealogy-paleographer`** | Primary scan retrieval, high-DPI plate cropping, cursive transcription, and microfilm offset checking. |
| **Tier 3** | **`genealogy-disambiguator`** | Metes-and-bounds survey platting, watercourse clustering, and annual tax list same-name separation. |
| **Tier 4** | **`genealogy-compiler`** | Wiki profile generation, scholarly monograph drafting, and *Evidence Explained* citation formatting. |
| **Tier 5** | **`genealogy-verifier`** | Adversarial Genealogical Proof Standard (GPS) auditor issuing strict `PASS`/`FAIL` sign-offs. |

---

## Chained Multi-Agent Workflow Pipeline

Each platform installer includes an automated workflow pipeline that chains these agents together in sequential and parallel stages:

```
[ Research Target / Question ]
               │
               ▼
┌──────────────────────────────┐
│ Phase 1: Director            │  (Scopes jurisdiction, film numbers, acceptance criteria)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Phase 2: Paleographer        │  (Extracts high-resolution scan & verbatim transcription)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Phase 3: Disambiguator       │  (Correlates survey bearings, tax lists, and FAN Club neighbors)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Phase 4: Compiler            │  (Updates wiki person profile, evidence logs & citations)
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Phase 5: Verifier (Auditor)  │  (Adversarial GPS review against primary scans -> PASS/FAIL)
└──────────────┬───────────────┘
               │
               ▼
[ Verified Proven Lineage Record Committed ]
```
