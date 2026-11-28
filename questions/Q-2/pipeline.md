---
question: Q-2
---

# Q-2 Pipeline Record

Branch: `q/2-adair-censuses-collaterals` (created 2026-11-28 from main at efda738)

| Stage | Gate | Result |
|---|---|---|
| 0 repo | Repo initialized; issue #2 read in full (body, criteria, labels, comments) | pass — 2026-11-28, lead via GitHub connector. Repo layout is the gen-NN alias layout (`people/gen-05-…`), not P- IDs; use the repo's actual layout. |
| 1 plan | plan.md complete; Alex approved (H0) | pass — plan approved by Alex 2026-11-28, including hard-stop defaults recorded in plan.md |
| 2 search | Every record group searched or blocked with logged entry | in progress — M-1 (1880) run 2026-11-28 and logged; M-2…M-5 requests committed with this push |
| 3 ingest | Zips ingested; transcriptions verified against full images | in progress — M-1 ingested 2026-11-28; 1880 transcription verified by the lead from the full image (`source-1880-census-ed1.md`) |
| 4 analysis | analysis.md with ## Conflicts (C1: John D. vs John M.) | pending |
| 5 proof | proof.md with conclusion_confidence, or stalled + settling record | pending |
| 6 review | review.md verdict pass (required only if proven claimed) | pending |
| 7 validate | Manual gate checklist (genealogy_repo_validate_muse), zero errors | pending — manual check, not a script run |
| 8 knowledge | knowledge: | pending |
| 9 close | plan.md status resolved/stalled; PR opened; closing comment posted; PR merged once gates pass (blanket approval incl. merge, Alex 2026-11-28) | pending |

Stage 1 note (2026-11-28): first `create_branch` attempt returned 403 "Resource not accessible by integration" (GitHub App had no write access to the repo). Alex granted all repos in the app installation, and the branch was created from main at efda738. These question files were drafted locally first, then committed in one snapshot push.

Stage 3 note (2026-11-28): the 1880 sheet image (1.9 MB JPG) is held in the question inbox, not committed — the GitHub connector's file writes are text-only, so binary plates cannot be pushed from Muse. The full citation and FamilySearch ARK in `source-1880-census-ed1.md` make the image retrievable; adding it under `sources/ky-adair/` can be done from a local checkout.
