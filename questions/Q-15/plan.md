---
question: Q-15
status: stalled
issue: https://github.com/alexcook-xyz/cook-lineage-research/issues/15
---
# Plan: Records bridging George Cook's 1771 Prince Edward exit and Sandy Creek, 1771–1782

## Objective
Identify primary records that place George Cook (Jr. and/or Sr.) and Electious Musick between the last Prince Edward sale (1771) and their Sandy Creek, Pittsylvania County presence (1780–1783), and test whether George Cook Jr. is the son of the Prince Edward George Cook (Gen 9) and George Cook Sr. is the father of George Cook Jr. (Gen 8 ← Gen 9 link).

## Known facts
| Fact | Source | Confidence |
|---|---|---|
| George Cook of Prince Edward sells 150 ac on Harris's Creek to Alexander Guill, 18 Apr 1768 | Prince Edward DB 3:366–368 | Verified from the image (M-2): deed is at DB 3:366-368; also acknowledged at OB 4:102 |
| George Cook sells Prince Edward land, 6 Apr / 16 Sep 1771 | DB 5:67–68 (per issue #15) | Unverified in repo; image not yet archived |
| Electious Musick Sr. sells 97 ac on Sandy Creek to George Cooke Jr., 2 Mar 1780 | Pittsylvania DB 6:34–35; `sources/va-pittsylvania/PITT_DB6_p34-35_Musick_to_CookeJr_1780.jpg` | Proven (image in repo; confirm transcript against image) |
| George Cook Jr. and Ruth sell ~100 ac on Sandy Creek to George Cook Sr., 9 Aug 1783 (proved 19 Aug 1783) | Pittsylvania DB 7:106–107; `sources/va-pittsylvania/PITT_DB7_p106-107_CookJr_to_CookSr_1783.jpg` | Proven (image in repo); no relationship stated |
| Ruth does not sign the 1783 deed | DB 7:106–107 (findings file) | Proven as recorded |
| George Cook Sr. 7 white souls, George Cook Jr. 4 white souls, Elijah Cook 4 white, 1782 | Virginia state enumeration 1782 (published) | Proven (published list; verify against original) |
| George Cook Sr. will proved 21 Sep 1835 | Pittsylvania WB 1:293 (index only) | Proven as index; will text restricted |
| Prior sweep found no primary record of George Cook in Prince Edward after 1768 in online sources | research/pre1780-sweeps/bridge_1768_1780_sweep.md | Negative sweep (online only) |

**Correction to issue #15:** the issue says high-res scans of DB 6:34–35 and DB 7:106–107 are not archived. The repo already holds them in `sources/va-pittsylvania/`. Remaining work is to confirm verbatim transcriptions against those images, not to retrieve them.

## Hypotheses
1. **H1 (migration corridor):** George Cook of Prince Edward (1768–1771) moved to Pittsylvania/Sandy Creek by 1780, and George Cook Jr. is his son.
2. **H2 (different George Cook):** George Cook Jr. on Sandy Creek is unrelated to the Prince Edward George Cook; the name recurrence is coincidental.
3. **H3 (null, no presence):** No record in 1771–1779 places George Cook in Pittsylvania, Lunenburg, Halifax, Caswell, Orange, or Granville between 1771 and 1780. (Resolved only after every group below is searched or blocked, per R2.)
4. **H4 (Sr. relationship):** George Cook Sr. is the father of George Cook Jr. (Gen 8 ← Gen 9 link is on the Sr. branch via Jr., or Sr. is a separate purchaser). This plan tests the Jr.–Sr. relationship only as far as the 1771–1782 records allow.

## Jurisdictions
| Place | Date range | Record-holding jurisdiction | Known losses |
|---|---|---|---|
| Prince Edward Co., VA | 1754–1800 | Prince Edward Co. Court (deeds, order books) | Some order books missing pre-1775 (verify) |
| Pittsylvania Co., VA | 1767–present | Pittsylvania Co. Court; Sandy Creek within Camden Parish (per DB 7 text) | Pre-1782 tithables and some early order books may be missing (verify) |
| Lunenburg Co., VA | 1746–present | Lunenburg Co. Court | Verify burned-county status |
| Halifax Co., VA | 1752–present | Halifax Co. Court (parent of Pittsylvania until 1767 division) | Verify |
| Caswell / Orange / Granville Cos., NC | 1771–1785 | NC county courts; Orange Co. records held at NC State Archives | Verify NC borderland losses |
| Virginia state | 1777–1785 | Virginia State Land Office (grants); Auditor's office (enumerations) | Enumerations incomplete for some counties |

## Record groups and search order
| # | Record group | Repository / collection | Tests hypothesis | Access | Assigned |
|---|---|---|---|---|---|
| 1 | Verbatim check of Pittsylvania DB 6:34–35 and DB 7:106–107 against archived images | `sources/va-pittsylvania/` (local) | H1, H4 (anchors the 1780/1783 facts) | Local, free | records-searcher |
| 2 | Prince Edward DB 5 (1771) original image for the 6 Apr / 16 Sep 1771 sale | Prince Edward Co. deed books, FamilySearch/LVA | H1 (exit date and buyer) | Free online if digitized; otherwise record request | records-searcher |
| 3 | Pittsylvania DB 1–5, order books, entry books, 1767–1782 | FamilySearch / LVA microfilm | H1, H2, H3 (first arrival date on Sandy Creek) | Free online; microfilm loan if not digitized (H3 trigger if blocked) | records-searcher |
| 4 | Pittsylvania 1777 Oath of Allegiance and tithables, 1777–1782 | LVA / Pittsylvania Co. | H1, H3 (presence in county) | Free online or microfilm | records-searcher |
| 5 | Lunenburg DB 1–13 and Sunlight on the Southside (1748–1783) | LVA / FamilySearch | H1, H3 (Cook or Musick presence in the 1771–1780 gap) | Free online where digitized | records-searcher |
| 6 | Caswell, Orange, Granville Cos., NC, 1771–1785 (deeds, court minutes, tax lists) | NC State Archives / FamilySearch | H1, H3 (state-line presence) | Free online where digitized; otherwise remote request | records-searcher |
| 7 | Virginia state enumerations and land grants, 1782–1785 (cross-check for Musick and Cook household sizes) | Published state lists; LVA Reel 56 | H4 (household grouping) | Free | records-searcher |
| 8 | Musick family records, Pittsylvania and Prince Edward (Electious Musick Sr. land and court records) | Pittsylvania and Prince Edward deeds | H1 (migration companion) | Free online | records-searcher |

Any record in groups 2–6 that needs an order, interlibrary loan, or visit opens a `record-retrieval` issue (labels `missing-record`, `remote-request`) and is logged with Result `needs remote request`. Do not place orders.

## FAN cluster
Electious (Elexius) Musick Sr., Elijah Cook, James Holloway, Joseph Flippen, Thomas Flippin, William Collie, Elisha Cooke, Ben Echols, Alexander Guill (Prince Edward buyer, 1768). Search each for co-location with Cook in 1771–1782.

## Done when
- **Resolved:** a dated primary record settles H1 or H2 for George Cook Jr. (Prince Edward 1771 sale to Sandy Creek 1780 linked by name, place, and a relationship clue or identity argument), and H3 is resolved (every group searched or blocked, no hit). Relationship to Sr. stated as proven, probable, or possible with the evidence graded.
- **Stalled (R3):** every group that could settle H1 or H2 is blocked (H3 open) and no free source remains. Name the settling record (specific reel, book, page) and the retrieval issue number in `proof.md` or this plan.
