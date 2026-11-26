import subprocess

milestone_titles = {
    1: "Milestone 1: Kentucky Line Completeness & Collateral Verification (Gen 1-6)",
    2: "Milestone 2: Resolve Generation 7 to 8 Bridge (Pittsylvania Co., VA, 1780-1837)",
    3: "Milestone 3: Pre-1780 Southside Piedmont Migration Bridge (1750-1780)",
    4: "Milestone 4: Colonial Roots to Immigrant Arrival (Pre-1750)"
}

issues = [
    # Milestone 1 Issues
    {
        "title": "[Record Pull]: Certified Marriage Certificate of Russell Cook & Anna Bell Sneed (c. 1934)",
        "milestone": 1,
        "labels": "missing-record,gen-1-6",
        "body": """### Research Question
Where and when did Russell Cook marry Anna Bell Sneed (or Hunt), and what official parentage names are stated?

### Why It Connects the Line
Arlin Cook's Social Security Numident lists his parents as `Russel Cook` and `Anna B. Sneed`. However, family archival holdings preserve an older portrait labeled `Hunt`. Obtaining the original county marriage bond and certificate (Adair, Taylor, Green, or Casey County, KY) reconciles the maternal lineage conclusively.

### Exact Repository & Citation Target
- County Clerk's Office: Adair, Taylor, or Green County, Kentucky.
- Marriage Register searches for Russell Cook (groom) between 1933 and 1935.

### Acceptance Criteria ("Definition of Done")
1. Primary scan of marriage bond, license, and return obtained.
2. Full transcription entered into `evidence/ky-modern/`.
3. Sneed vs. Hunt maternal relationship resolved without speculative assertions.

### Known Traps to Avoid
- Do not confuse with Russell Cook of Ohio or Western Kentucky.
- Watch for phonetic transcription variants (`Snead`, `Sneed`)."""
    },
    {
        "title": "[Record Pull]: Microfilm Schedules for Adair County Censuses 1880–1930 (George W. Cook Collaterals)",
        "milestone": 1,
        "labels": "missing-record,gen-1-6",
        "body": """### Research Question
How do the collateral households of George William Cook (1852–1935), Thomas H. Cook, and John D. Cook track across Adair County between 1880 and 1930?

### Why It Connects the Line
Corroborates the family structure established in Eliza E. Cook's will (WB M:133–134) and verifies that George William Cook remained continuously on the family's Russell's Creek home tract.

### Exact Repository & Citation Target
- National Archives & Records Administration (NARA) Microfilm: Adair County, KY (1880, 1900, 1910, 1920, 1930).

### Acceptance Criteria ("Definition of Done")
1. Complete household enumeration sheets retrieved for District 1/2 (Columbia / Russell's Creek).
2. Verbatim transcriptions stored in `research/`.

### Known Traps to Avoid
- Avoid Ancestry index inversions (e.g., treating mother Eliza Cole as spouse)."""
    },
    {
        "title": "[Record Pull]: Cumberland County, Kentucky Tax Lists 1833–1845 for George & Henry Cook",
        "milestone": 1,
        "labels": "missing-record,gen-1-6",
        "body": """### Research Question
When did brothers George Cook and Henry Cook first appear in Cumberland County, Kentucky, and when did George transition across the county line into Adair County?

### Why It Connects the Line
On 2 November 1836, George and Henry Cook executed a Power of Attorney in Cumberland County, Kentucky (Pittsylvania DB 39:242) authorizing their brother James Cook of Adair County to sell their inherited interest in George Cook's 277-acre Virginia estate.

### Exact Repository & Citation Target
- Kentucky Historical Society / FamilySearch Microfilm: Cumberland County Tax Books (1833–1845).

### Acceptance Criteria ("Definition of Done")
1. Year-by-year tithable count, land acreage, and watercourse locations extracted.
2. Confirms exact age of majority (turning 21) for George Cook (c. 1834)."""
    },

    # Milestone 2 Issues
    {
        "title": "[P0 In-Person Pull]: Pittsylvania County Will Book 1, pp. 293–294 (George Cook Sr. Will, 1835)",
        "milestone": 2,
        "labels": "blocked-film,in-person-archive,gen-7-8,hypothesis-test",
        "body": """### Research Question
What are the verbatim contents and specific bequests of George Cook Sr.'s will, proved 21 September 1835 in Pittsylvania County?

### Why It Connects the Line
George Cook Sr. is the 1835 testator whose 97-acre Sandy Creek tract was sold by Sheriff Thomas H. Wooding c.t.a. in January 1837 (DB 39:319–320). Reading this will directly is the critical test to prove whether George Cook (\"George B,\" d. 1831) is his son and whether George B's orphaned children are named.

### Exact Repository & Citation Target
- Library of Virginia (Richmond, VA) or FamilySearch Center.
- FamilySearch Film #007642302 (Wills, Vol. 1–2, 1820–1860). Restricted digital access.

### Acceptance Criteria ("Definition of Done")
1. High-resolution photocopy or digital camera capture of WB 1:293–294.
2. Complete verbatim transcript placed in `evidence/va-pittsylvania/`.
3. Determination whether Gen 7 → 8 moves from working hypothesis (~75–80%) to fully proved.

### Known Traps to Avoid
- Do not accept the 67-image index on Ancestry; the actual will text is excluded from digitized collections."""
    },
    {
        "title": "[In-Person WKU Check]: Print Volume 'Marriages of Pittsylvania County, Virginia, 1806–1830'",
        "milestone": 2,
        "labels": "in-person-archive,gen-7-8",
        "body": """### Research Question
Does Kathleen Booth Williams' print register record a marriage bond for George Cook to Catharine (c. 1806–1818)?

### Why It Connects the Line
Catharine Cook was the widow of George Cook in the 15 October 1831 estate deed (DB 33:101). Her maiden surname remains unrecovered in all online commercial databases.

### Exact Repository & Citation Target
- Western Kentucky University (WKU) Special Collections Library, Bowling Green, KY.
- Call Number / Book: *Marriages of Pittsylvania County, Virginia, 1806–1830* (Kathleen Booth Williams, 1980).

### Acceptance Criteria ("Definition of Done")
1. Physical volume checked page-by-page.
2. Full citation and excerpt added to repo.

### Known Traps to Avoid
- George Cook appears as bondsman in 1815 and 1819; confirm groom identity specifically."""
    },
    {
        "title": "[Record Pull]: Pittsylvania County Mixed Probate Books 3 & 7 and Accounts Current Book 3, p. 264",
        "milestone": 2,
        "labels": "missing-record,in-person-archive,gen-7-8",
        "body": """### Research Question
What estate settlements, account audits, and orphan guardian distributions are recorded in Pittsylvania Mixed Probate Books 3 and 7?

### Why It Connects the Line
Accounts Current Book 7:210–211 preserves the 1823 inventory of George Cook returned by Richard B. Cook. Checking the separate Mixed Probate series and Elijah Cook's 1804 division (AC 3:264) clarifies the broader sibling network and guardian accounts.

### Exact Repository & Citation Target
- Pittsylvania County Courthouse / Library of Virginia microfilm.

### Acceptance Criteria ("Definition of Done")
1. Scans or photocopies of estate settlements secured.
2. Documented in `evidence/va-pittsylvania/`."""
    },
    {
        "title": "[Disambiguation]: Annual Pittsylvania County Land & Personal Property Tax Lists (1782–1837)",
        "milestone": 2,
        "labels": "disambiguation,hypothesis-test,gen-7-8",
        "body": """### Research Question
How do the 4 to 5 concurrent adult men named George Cook in Pittsylvania County track year-by-year across separate tax districts?

### Why It Connects the Line
Disambiguates George Cook Sr. (Sandy Creek), George Cook Jr. / George B (Dan River / Sandy Creek), George Cook (Pigg River / Banister), and George Cook (Chancery 143-1840-024 poorhouse plaintiff).

### Exact Repository & Citation Target
- Library of Virginia Microfilm: Pittsylvania County Personal Property Tax Lists (1782–1837) and Land Tax Books.

### Acceptance Criteria ("Definition of Done")
1. Master comparative tax tracking table created in `research/`.
2. Each George Cook assigned to his distinct watercourse."""
    },

    # Milestone 3 Issues
    {
        "title": "[Record Pull]: Prince Edward County Deed Books 3–7 (Disposition of 250 Acres on Harris's Creek)",
        "milestone": 3,
        "labels": "missing-record,pre-1780",
        "body": """### Research Question
How did George Cook dispose of the remaining 250 acres of his 1750 patent on Harris's Creek after selling 150 acres to Alexander Guill in 1768?

### Why It Connects the Line
On 18 April 1768, George Cook sold 150 acres on Harris's Creek (DB 3:366–368). Finding the conveyances for the remaining 250 acres establishes his departure date from Prince Edward County prior to his appearance on Sandy Creek in Pittsylvania County.

### Exact Repository & Citation Target
- Prince Edward County Courthouse / Library of Virginia Microfilm (Deed Books 3, 4, 5, 6, 7; 1768–1785).

### Acceptance Criteria ("Definition of Done")
1. Identification of all subsequent conveyances citing Harris's Creek adjoining Lockett and Jones.
2. Primary deed images deposited in `evidence/va-colonial-lva/`."""
    },
    {
        "title": "[Record Pull]: Prince Edward & Amelia County Court Order Books 1750–1775",
        "milestone": 3,
        "labels": "missing-record,pre-1780",
        "body": """### Research Question
What civil suits, tithable lists, road orders, and grand jury presentments mention George Cook in Prince Edward and parent Amelia County?

### Why It Connects the Line
Establishes the timeline of residency, church parish affiliation (Nottoway / St. Patrick's Parish), and economic associations before the migration into the Dan River basin.

### Exact Repository & Citation Target
- Library of Virginia: Amelia Court Orders (1745–1754) and Prince Edward Order Books 1–7 (1754–1780).

### Acceptance Criteria ("Definition of Done")
1. All order book entries transcribed with volume and page citations."""
    },
    {
        "title": "[Record Pull]: Halifax County, Virginia Deed Books 1–10 & Plea Books 1–9 (1752–1775)",
        "milestone": 3,
        "labels": "missing-record,pre-1780",
        "body": """### Research Question
Did George Cook, Josiah Cook, or Zachariah Cook own land or litigate in Halifax County prior to the 1767 creation of Pittsylvania County?

### Why It Connects the Line
Pittsylvania was formed directly from Halifax in 1767. Any Cook records on Sandy Creek, the Dan River, or the Banister River prior to 1767 will be found in Halifax County.

### Exact Repository & Citation Target
- Halifax County Courthouse / Library of Virginia Microfilm: Halifax Deeds 1752–1767, Pleas 1752–1767.

### Acceptance Criteria ("Definition of Done")
1. Verification of Zachariah Cook's estate proceedings (c. 1767) and early Dan River surveys."""
    },

    # Milestone 4 Issues
    {
        "title": "[Archival Search]: Virginia Land Patents 1–28 (1623–1749) for Early Southside Cook Patents",
        "milestone": 4,
        "labels": "missing-record,immigration",
        "body": """### Research Question
Which early colonial Virginia patentee or headright represents the progenitor of George Cook of Amelia County (1750 patentee)?

### Why It Connects the Line
The 1750 patent to George Cook (Patents 29:316–317) was granted by President Thomas Lee for 40 shillings. Tracing earlier patents across Prince George, Surry, and Isle of Wight counties identifies the earlier family roots.

### Exact Repository & Citation Target
- Library of Virginia Colonial Land Office Patent Books 1 through 28.
- *Cavaliers and Pioneers* (Nell Marion Nugent), Vols. 1–5.

### Acceptance Criteria ("Definition of Done")
1. Comprehensive spreadsheet of all colonial Cook land grants along the Appomattox and James rivers."""
    },
    {
        "title": "[Archival Search]: Colonial Emigrant & Port Records for Cook Arrivals into Virginia & Maryland",
        "milestone": 4,
        "labels": "missing-record,immigration",
        "body": """### Research Question
What documented British port departures match the earliest Southside Virginia Cook settlers?

### Why It Connects the Line
Final link connecting the Virginia colonial patrilineal line across the Atlantic to British origin.

### Exact Repository & Citation Target
- Peter Wilson Coldham, *The Complete Book of Emigrants* (1607–1776).
- Gust Skordas, *The Early Settlers of Maryland*.
- National Archives (UK) Kew: High Court of Admiralty (HCA) and Port Books.

### Acceptance Criteria ("Definition of Done")
1. Evaluated candidate list of 17th-century Cook immigrants correlated against Tidewater patent headrights.
2. Explicitly avoids speculative connections without primary chain-of-title or probate proof."""
    }
]

for issue in issues:
    m_title = milestone_titles[issue["milestone"]]
    cmd = [
        "gh", "issue", "create",
        "--repo", "alexcook-xyz/cook-lineage-research",
        "--title", issue["title"],
        "--body", issue["body"],
        "--milestone", m_title,
        "--label", issue["labels"]
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Created issue: {res.stdout.strip()}")
    else:
        print(f"Error creating issue '{issue['title']}': {res.stderr}")
