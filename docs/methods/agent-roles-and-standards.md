# Professional Multi-Agent Architecture for Genealogical Research & Documentation

This specification defines the standard multi-agent architecture, division of responsibilities, evidentiary workflows, and quality gates for the **Cook Patrilineal Lineage Research Project**.

---

## 1. Industry Standard for Agentic Historical & Genealogical Research

Professional historical and genealogical inquiry operates under strict evidentiary rules (such as the Board for Certification of Genealogists' *Genealogical Proof Standard*). AI agents in this domain must not operate as monolithic generalists; doing so leads to:
1. **Hallucination of sources and citations** (e.g., inventing book numbers or will dates).
2. **Failure to catch index and microfilm offsets** (e.g., misreading digital film frame skips).
3. **Premature conclusions** (e.g., merging same-name individuals without tax and deed disambiguation).

To adhere to industry best practices, the research architecture divides responsibilities across five distinct tiers:
- **Tier 1: Coordination & Session Oversight**
- **Tier 2: Archival Retrieval & Paleographic Extraction**
- **Tier 3: Land, Probate & Disambiguation Analysis**
- **Tier 4: Synthesis, Documentation & Publishing**
- **Tier 5: Independent Verification & Evidentiary Quality Control (The Auditor)**

```
                      ┌─────────────────────────┐
                      │    RESEARCH DIRECTOR    │
                      │      (Coordinator)      │
                      └────────────┬────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ ARCHIVAL AGENT  │       │ ANALYSIS AGENT  │       │ COMPILATION     │
│ (Scraper / OCR) │       │ (Deeds/Tax/FAN) │       │ (Wiki/Paper/MD) │
└────────┬────────┘       └────────┬────────┘       └────────┬────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
                                   ▼
                      ┌─────────────────────────┐
                      │ INDEPENDENT VERIFIER    │
                      │  (GPS Quality Control)  │
                      └─────────────────────────┘
```

---

## 2. Standardized Agent Roles & Responsibilities

### Role 1: Research Director / Coordinator
- **Core Mission:** Orchestrates the research roadmap, defines specific hypothesis tests, assigns scope to specialist agents, and maintains repository issue boards.
- **Key Constraints:** Never performs heavy script edits or inline text drafting; focuses entirely on workflow orchestration, review of evidence, and user reporting.

### Role 2: Archival Retrieval & Paleography Specialist
- **Core Mission:** Locates, downloads, crops, and transcribes original court and state archive records (Deed Books, Will Books, Land Patents, Court Order Books, Tax Lists).
- **Core Methodology:**
  - Reads cursive legal hands verbatim, noting damaged margins, stamps, and clerk certifications.
  - Verifies folio numbers against microfilm binding sequences to detect page offsets and vendor indexing errors.
  - Generates high-DPI cropped documentary plates for public inspection.

### Role 3: Land, Tax & Disambiguation Specialist
- **Core Mission:** Solves same-name conflicts, plots metes-and-bounds deed surveys, and reconstructs community clusters (FAN Club: Friends, Associates, and Neighbors).
- **Core Methodology:**
  - Extracts survey bearing angles (`S 10° W`, `W 6° S 120 poles`) to prove land continuity across county splits.
  - Builds annual personal property and land tax tables to track concurrent men sharing identical names along distinct river basins.

### Role 4: Documentation & Monograph Compiler
- **Core Mission:** Synthesizes verified evidence into publication-ready research reports, wiki profiles, master lineage tables, and GitHub issue trackers.
- **Core Methodology:**
  - Formats all citations strictly according to *Evidence Explained* / *Chicago Manual of Style*.
  - Enforces neutral, evidence-driven prose without synthetic banners, fake journal mastheads, or personal thesis language.

### Role 5: Independent Evidentiary Verifier (GPS Auditor)
- **Core Mission:** Acts as an adversarial quality gate before any profile or generational link is marked as *Proven*.
- **Core Methodology:**
  - Performs cross-checks comparing drafted claims against original primary scans.
  - Verifies zero tolerance for unsupported generational leaps, unverified secondary trees, or prohibited topics.
  - Issues explicit `PASS` or line-by-line `FAIL` directives with exact correction requirements.

---

## 3. Standard Operating Procedures (SOP) for Evidence Progression

```
[ New Lead / Open Question ]
            │
            ▼
┌─────────────────────────┐
│ 1. Open GitHub Issue    │ ──> Categorized by Jurisdiction, Milestone & Exact Film/Volume
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 2. Archival Pull & Scan │ ──> Primary image placed in evidence/ with full folio check
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 3. Verbatim Transcript  │ ──> Paleographic transcription including witnesses and endorsements
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 4. Disambiguation Check │ ──> Tested against tax lists, watercourses, and same-name matrices
└───────────┬─────────────┘
            ▼
┌─────────────────────────┐
│ 5. Verifier Sign-off    │ ──> Independent verification against GPS criteria
└───────────┬─────────────┘
            ▼
[ Profile Updated: PROVEN / WORKING HYPOTHESIS ]
```
