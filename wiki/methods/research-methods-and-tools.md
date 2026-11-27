# Research Methods, Tools, and Evidentiary Procedures

This document outlines the professional genealogical research methodology, analytical tools, and investigative protocols utilized in the **Cook Patrilineal Lineage Research Project**.

---

## 1. Research Methodology

Our research methodology is modeled upon rigorous historical and legal evidentiary analysis:

### A. Reverse-Chronological Investigation
Genealogical proof proceeds strictly from the known present backward into the past:
- Never assume an identity or parentage in the colonial era and trace forward without first establishing an unbroken chain of title and vital records backward from the living subject.
- Each generation serves as the evidentiary anchor for the next.

### B. Original Record Inspection (Deed-and-Will Primacy)
- Secondary databases, user-contributed family trees (e.g., Ancestry trees, FamilySearch user trees), and published family genealogies are treated strictly as unverified clues, never as evidence.
- Every assertable date, acreage, relationship, and legal act must be verified against digital images or physical photocopies of the **original county court registers** (Deed Books, Will Books, Accounts Current, Order Books, Minute Books, and Tax Books).
- Microfilm roll offsets and volume binding anomalies must be documented folio-by-folio to guard against commercial digital scanning skips (e.g., the Adair County DB Z page 195 vs. 252 offset).

### C. Watershed & Watercourse Mapping
In colonial Virginia and frontier Kentucky, county boundaries frequently shifted, but creeks and river branches remained permanent:
- Every land transaction is plotted by its specific watercourse (e.g., Harris's Creek in Prince Edward/Amelia, Sandy Creek and Dan River in Pittsylvania, Russell's Creek in Adair).
- Neighboring landowners ("adjoiners") named in deeds provide the community cluster (the FAN Club: Friends, Associates, and Neighbors) that distinguishes men of the same name.

### D. Metes-and-Bounds Survey Angle Correlation
Where deeds do not explicitly name parental inheritance, survey bearings are mathematically checked:
- Compares boundary angles (e.g., `South 10 degrees West`, `West 6 degrees South 120 poles`) across decades and across county splits (e.g., matching the 1750 Amelia Patent to the 1768 Prince Edward Deed).

---

## 2. Research Tools & Technologies

| Tool / Technology | Purpose & Application in Project |
|---|---|
| **County Court Microfilm Readers & Scanners** | Pulling un-indexed and restricted courthouse records (FamilySearch Centers, Library of Virginia, Kentucky Department for Libraries and Archives). |
| **Library of Virginia (LVA) Digital Collections** | Accessing Land Office Patents (1623–1774), Commonwealth Land Grants (1779+), and Chancery Records Index (53 Pittsylvania Cook suits). |
| **ReportLab & Python Scripting (`scripts/`)** | Programmatic assembly and high-DPI cropping of documentary evidence plates into publication-quality research monographs without synthetic software watermarks. |
| **PyMuPDF / Pillow** | Extracting, inspecting, and enhancing high-resolution scans of 18th- and 19th-century cursive county records to make illegible script readable. |
| **GitHub Issues & Milestones** | Project tracking, archival pulling roadmaps, and systematic assignment of research tasks. |

---

## 3. Workflow for Adding a New Generation or Record

When a new archival document or generational link is proposed for the project:

1. **Open an Issue:** Submit an issue using `.github/ISSUE_TEMPLATE/record-retrieval.yml` specifying the jurisdiction, volume, folio/page, and research question.
2. **Retrieve Primary Scan:** Place the uncompressed digital capture in the appropriate `evidence/` folder.
3. **Full Verbatim Transcription:** Transcribe the complete legal instrument (including witness names, boundary descriptions, and court recording endorsements) rather than relying on an abstract.
4. **Disambiguation Check:** Cross-reference against concurrent same-name tax lists and deeds.
5. **Update Wiki Profile & Master Lineage Table:** Update the person's wiki markdown profile and commit the changes with a full source citation.
