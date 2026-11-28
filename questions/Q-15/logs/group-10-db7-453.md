# Q-15 research log, record group 10 (Pittsylvania Deed Book 7 images, Internet Archive items db7a_20260526 and db7b_20260527)

Searcher: records-searcher (agent). Date of all entries: 2026-11-28. Free Internet Archive items (uploader (IA uploader, Pittsylvania Circuit Court Clerk), 26-27 May 2026), "PittCoDB7A" and "PittCoDB7B", handwritten deed book images, no usable OCR. Downloads are untrusted; only single JPEG 2000 page images were pulled (about 3 MB each) from inside DB7A_jp2.zip and DB7B_jp2.zip with curl, converted with Pillow (python -I), and viewed with the image reader. The 1 GB PDFs were not downloaded. Working files: scratchpad ia-scans/db7-453/a and /b (not in the repo). No login, no payment.

### 2026-11-28 — Internet Archive db7a_20260526 / db7b_20260527: item metadata and page-to-leaf mapping
- **Searcher:** records-searcher
- **Goal:** Locate DB 7 p. 453 and p. 106-107 inside the two items; plan row 3.
- **Search terms:** metadata API; scandata; leaf probes DB7A 100, 246; DB7B 5, 100(not viewed), 219.
- **Coverage:** DB7A = 247 leaves; leaf 0100 = printed p. 88 (so DB7A leaf = page + 12 near pp. 88-107); leaf 0246 = about p. 234. DB7B = 253 leaves; leaf 0005 = p. 239; leaf 0219 = p. 451. Offset is not constant (the books have unnumbered leaves). No printed page numbers in IA metadata (page_numbers.json empty).
- **Result:** found
- **Findings:** p. 453 = DB7B leaf 0221; p. 454 = leaf 0222; p. 106 = DB7A leaf 0118; p. 107 = leaf 0119.
- **Index or original:** Original deed book images (clerk's fair copy), not an index.
- **Leads (not evidence):** none
- **Next:** read pp. 453-454, 107.

### 2026-11-28 — Pittsylvania DB 7:453-454 (DB7B leaves 0221-0222): Peter Martin to Elijah Cook, 4 Jun 1785
- **Searcher:** records-searcher
- **Goal:** Read the deed behind the Grantee Index entry "Elijah, 20 Jun 1785, from Peter Martin, B & S, 7:453"; plan rows 3, 8.
- **Search terms:** Cook, Elijah, Martin, Musick, Holloway, Flippin/Flippen on pp. 451-454.
- **Coverage:** pp. 453 (full page at 1300 px width plus an enlarged crop of the Martin deed) and 454 (full page) read. Pp. 451 and 452 viewed (451 at 700 px; 452 full) as neighbours.
- **Result:** found
- **Findings:** [[S-pittsylvania-db7-p453-454-martin-to-elijah-cook-1785]]. Key text: "Peter Martin of Halifax County and State of Virginia of the one part and Elijah Cook of Pittsylvania County and State aforesaid of the other part" ... "a tract or parcel of land in Pittsylvania County on Sandy Creek where Elijah Cook now lives containing by estimation fifty acres"; bounds run "to George Cooks (Senr) corner pine" and "to John Watters corner formerly called James Collies"; ten pounds Virginia currency; witnesses "Zachariah Butt, Uriah [his mark] Owen / George Cook Sener, John [mark] Everett"; proved 20 Jun 1785 by three witnesses. Peter Martin signs by mark. No Musick, Holloway or Flippin name on pp. 451-454. No relationship statement between Elijah and George.
- **Index or original:** Original deed book image.
- **Leads (not evidence):** none
- **Next:** Elijah's 1782 household (4 white) and George Sr.'s adjoining land (corner pine) can be tied to the Sandy Creek plats; look for Peter Martin of Halifax in Halifax deeds (not done).

### 2026-11-28 — Pittsylvania DB 7:106-107 (DB7A leaves 0118-0119): re-read of the court year digit and testimonium
- **Searcher:** records-searcher
- **Goal:** Settle the court-endorsement year digit and the testimonium word ("Junor" or "Senor") left uncertain in S-pittsylvania-db7-p106-107-cook-jr-to-cook-sr-1783; plan row 1.
- **Search terms:** p. 107 testimonium; court endorsement; witnesses.
- **Coverage:** p. 107 read in full at 1300 px, with 3x enlargements of the testimonium and the court-date line. p. 106 not re-viewed (leaf 0118 downloaded only).
- **Result:** partial
- **Findings:** [[S-pittsylvania-db7-p107-reread-ia-leaf119-1783]]. Court year: "At a Court held for Pittsylvania County the 19th Day of August 178[?]" with the last digit cut off at the right edge of this image as well; not readable. Testimonium: "In Witness whereof the said George Cook [Junor or Senor] and Ruth his wife Have hereunto Set there Hands and Seals the Day and year above Written"; my reading of the word is "Junor" (about 60 percent), opposite to the earlier reading "Senor"; uncertain, second reader needed. Witnesses re-confirmed: Wm. Hedgpeth, Joseph Flippen, James Holloway, Elijah Cook, Orlando Smith. Ruth does not sign.
- **Index or original:** Original deed book image.
- **Leads (not evidence):** none
- **Next:** Year digit may be read from the Order Book entry for 19 Aug 1783 (not searched) or from the neighbouring deeds on p. 106 and 108 that share the same court day; the next deed on the page after 107 would carry the same court day.

### 2026-11-28 — Other DB 7 pages opened for calibration
- **Searcher:** records-searcher
- **Goal:** Find Cook, Musick, Holloway, Flippin names on pages opened; row 3.
- **Search terms:** same names.
- **Coverage:** DB7A leaf 0100 (p. 88, Warren to Jenkins, 19 Aug 1783, first page only legible part), leaf 0246 (Holland to Shockley, Sept 1783 / Slayden to Mann, 27 Mar 1784), DB7B leaf 0005 (p. 239, Slayden to Colley), leaf 0219 (p. 451, Bobbett to Bobbett / Devan bill of sale). Viewed at 700 px, not transcribed.
- **Result:** nothing found
- **Findings:** No Cook, Musick, Holloway or Flippin name seen on those pages (reading at 700 px only; not a line-by-line search). Court-day on p. 88 is 19 Aug 1783, the same day as the Cook Jr. deed proof.
- **Index or original:** Original images.
- **Leads (not evidence):** none
- **Next:** none
