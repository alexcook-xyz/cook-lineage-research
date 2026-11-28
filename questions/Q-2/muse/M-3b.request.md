# M-3b — Q-2 — 1910 U.S. Census, Adair County, Kentucky — collection-filtered survey completion

Status: **ingested** — run 2026-11-28 (cloud browser, 13:23–13:26 CST). Collection filter worked first attempt (41 results, 23 Adair). No John (adult) and no Laura in Adair in 1910; one adjacent-county lead (John B. Cook, Green Co.) held unassigned. No downloads. Full entry: log.md, search 6.

## GOAL

Complete the 1910 Adair County coverage for Q-2: (1) a true collection-filtered list of every Cook/Cooke person in Adair County, KY in the 1910 census index; (2) dedicated 1910 searches for John Cook (D. or M.) and Laura (B.) Cook in Adair County.

## RULES (non-negotiable)

1. READ-ONLY. Change nothing in any account. Do not save, attach, edit, or accept anything into any tree.
2. At most 3 agents in own tabs; 25 page views total.
3. Download the actual image file (JPG) via the viewer's Download control ONLY if a search finds a 1910 Adair household of John Cook or Laura Cook that fits the targets (John: son of Eliza, b. 1840s–1850s KY, parents VA/KY or VA/VA; Laura: daughter of Eliza, b. ~1867–1870 KY). Otherwise no downloads — index-level identification is the deliverable.
4. Ancestry (signed in on the device browser) is a lead source only: its 1910 index may be used to pin ED/sheet for a John or Laura hit; the image, if any, comes from FamilySearch. Never cite the Ancestry index or copy its relationship labels.
5. Never use Newspapers.com.
6. Return the result as `M-3b.result.md` (plus `M-3b_1_image.jpg` etc. only if a sheet is downloaded, listed in a FILES table).
7. Stop and report on: login wall with no working sign-in, paywall, CAPTCHA you cannot clear, or the page-view cap.
8. Do not infer. Report index data exactly as shown; mark uncertain readings [?].

## METHOD (use this — it is the route that worked for 1900)

FamilySearch record search with the collection filter as a URL parameter:
`https://www.familysearch.org/en/search/record/results?count=100&q.surname=Cook&q.residencePlace=Adair%2C%20Kentucky%2C%20United%20States&f.collectionId=1727033`
(1727033 = "United States Census, 1910".) First check the result count: a correct filter gives a small set (tens, not hundreds of thousands). If it returns 0, retry once with the residence place spelled "Adair, Kentucky" and once via the search UI's Collection filter; report which form worked. Repeat for surname Cooke.

## TASKS

1. **Filtered survey:** every Cook, then every Cooke, in Adair County in the 1910 collection — name, birth year as indexed, census place/ED as shown.
2. **John search:** John Cook (and John D. / John M. variants), 1910 census, Adair County; also any Kentucky-born John Cook aged 50–70 in the 1910 census whose residence is Adair or an adjacent county (Casey, Russell, Cumberland, Metcalfe, Green, Taylor) — adjacent-county hits are leads, reported as such.
3. **Laura search:** Laura Cook in Adair County, 1910 census (she was Laura B. Cook, b. Dec 1870 per 1900, in her mother's household in 1900 and not with George in 1910). If she is not in Adair under Cook, say so on the filtered survey's coverage.

## RESULT FORMAT (M-3b.result.md)

Sections: SUMMARY (one line: filtered-survey count + whether John or Laura was found in Adair in 1910) / SURVEY (table: name, birth, place, ED) / JOHN (result with ARKs, or not-found with coverage) / LAURA (same) / DOWNLOADS (any sheet downloaded, or "none") / STOPS (any rule-7 stop hit, or "none").
