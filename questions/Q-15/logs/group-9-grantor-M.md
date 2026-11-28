# Q-15 research log, record group 9 (Pittsylvania Co., VA Grantor Index 1765-1889, letter M: Musick / Music / Muzick / Mewsick)

Searcher: records-searcher (agent). Date of all entries: 2026-11-28. Free source (Internet Archive scan, https://archive.org/details/grantor-index-june-1765-1889, downloaded with the user's approval; untrusted file, handled only with pdfinfo/pdftoppm and `python3 -I` for image crops, nothing run from its directory). Plan rows 8 and 3. Source created: [[S-pitt-grantor-index-m-p36-musick-1780-1781]].

Working files (not part of the repo): PDF `(local scratch directory, not in repo)` (115 pages, image only); renders in `.../scratchpad/ia-index/pages-grantor-M/` (50 dpi surveys, 110 dpi for PDF pp. 109-111, a crop of p. 110).

Volume structure: Cott ledger, grantor index; columns date of record, surname, given names (three columns by initial), grantee, kind of instrument, volume (deed book), page. Alphabetical by surname, then chronological. Ledger page numbers restart by section: PDF p. 100 = ledger p. 26 (Motley 1883-87), PDF p. 108 = ledger p. 34 (Muse), PDF p. 110 = ledger p. 36, PDF p. 111 = ledger p. 37, PDF p. 112 = ledger p. 38.

### 2026-11-28 — Internet Archive scan: Pittsylvania Grantor Index, letter M, binary search for Mus- run
- **Searcher:** records-searcher
- **Goal:** Locate the Musick pages by alphabetical binary search; plan rows 8, 3.
- **Search terms:** page headers and first surnames at 50 dpi
- **Coverage:** PDF pp. 90, 100 (Motley), 104, 107, 108 (Muse 1806-1871), 110 (Muse 1889; Musgrove; Musick; Mustain from 1756), 113, 115 opened at survey resolution (90, 104, 107, 113, 115 rendered but only 100, 108, 110 viewed in detail).
- **Result:** found (location only)
- **Findings:** Musick falls on PDF p. 110 (ledger p. 36), between Musgrove and Mustain.
- **Index or original:** Index (typed ledger). Deeds not seen.
- **Leads (not evidence):** none
- **Next:** read PDF pp. 109-112 in full (next entry).

### 2026-11-28 — Internet Archive scan: Pittsylvania Grantor Index M, Mus- run, read for Musick / Music / Muzick
- **Searcher:** records-searcher
- **Goal:** Read every Musick entry, any year 1767-1790; flag Electious/Elexius/Electius, George, Dextrous, Abram; plan rows 8, 3.
- **Search terms:** Surnames Musick, Music, Muzick, Musik, Mewsick; given names Electious, Elexius, Electius, Elexicous, Elixicous, George, Dextrous, Abram, Abraham.
- **Coverage:** PDF p. 110 read at 110 dpi (Musick rows and crop); PDF p. 111 (Mustain 1836-1871) read at 110 dpi; PDF p. 112 (Mustain 1872-1889, Mustaine, Musteen, Mustean, Myers, Myer) read at 50 dpi. PDF p. 109 was rendered at 110 dpi but not viewed: the Muse run before Musgrove is not relevant to Musick (see Muse note below). Index runs in order Muse, Musgrove, Musick, Mustain, so no "Music/Muzick" lines elsewhere in the run. The index gives only two Musick lines for all years.
- **Result:** found
- **Findings:** Two entries, both grantor "Musick" (verbatim from the image):

  | Date of record | Grantor | Grantee | Instrument | Deed book : page | Flag |
  |---|---|---|---|---|---|
  | 15 Aug 1780 | Musick, Electious Sr | George Cooke Jr | B & S | 6 : 34 | Electious; George (grantee, Cooke Jr). Matches the repo anchor DB 6:34-35 (dated 2 Mar 1780 in its text) |
  | 18 Apr 1781 | Musick, "(Elexicous / Elixicous or" | John Johnson | B & S | 6 : 93 | Elexius variant; NEW citation, not previously in the repo |

  No Musick grantor entry for George, Dextrous or Abram; no entry for any year other than 1780 and 1781. Source: [[S-pitt-grantor-index-m-p36-musick-1780-1781]].
- **Index or original:** Index only (typed 1934 Cott ledger). Deed images not seen.
- **Leads (not evidence):** The 1783 land alterations list in the repo ([[S-pitt-land-alterations-1783-vagenweb]]) has "John Johnson 304 Abram Musick", which may relate to the 1781 John Johnson purchase; this is a lead, not established.
- **Uncertain readings:** (1) the 1781 given-name cell, typed on two lines as "(Elexicous" and "Elixicous or"; legible at 110 dpi, but what the typist meant (a variant pair? "Elexicous or Elixicous"?) is unclear; read with high confidence as typed. (2) The index is a later compilation; the 15 Aug 1780 date of record against the deed's 2 Mar 1780 date is unverified, and the vol/page figures were read at 110 dpi (high confidence).
- **Next:** pull Deed Book 6:93 (Musick to John Johnson, recorded 18 Apr 1781) and re-read 6:34 recording endorsement; see the grantee index (group-9-grantee-M.md) for Cooke/Johnson as grantee (volumes C and J).

### 2026-11-28 — Internet Archive scan: Pittsylvania Grantor Index M, Mewsick spelling
- **Searcher:** records-searcher
- **Goal:** Check Mewsick/Mewsic placement; plan row 8.
- **Search terms:** Mewsick, Mewsic, Meusick (would sort after Metts/Meux, before Meyer)
- **Coverage:** PDF pp. 40, 45, 50, 51-54, 56, 57, 60, 70, 80 at 50 dpi (crops of the left columns only). PDF p. 54 shows Merriman/Merrett/Merritt/Merrix/Metts/Meux/Meyer/Myers: no Mewsick. Pages 51-54 viewed in reduced crops (left ~330 px), so surnames legible but not every row of every page was checked beyond the visible crop; PDF p. 55 is a Cott buff instruction sheet, not index rows.
- **Result:** nothing found
- **Findings:** No Mewsick or similar line in the Me run at the position where it would sort.
- **Index or original:** Index.
- **Leads (not evidence):** none
- **Next:** none for this volume.

### 2026-11-28 — Internet Archive scan: Pittsylvania Grantor Index M, pages not read
- **Searcher:** records-searcher
- **Goal:** Record coverage gaps.
- **Search terms:** n/a
- **Coverage:** Not read: PDF pp. 2-39, 41-44, 46-49, 58-59, 61-69, 71-79, 81-99, 101-103, 105-107, 109 (rendered, not viewed), 113-115 (113, 115 rendered only). None would hold Musick/Music/Muzick/Mewsick by alphabet. Surname cells under "do" (ditto) on p. 110 were checked as Musick.
- **Result:** partial
- **Findings:** none.
- **Index or original:** Index.
- **Leads (not evidence):** none
- **Next:** none.
