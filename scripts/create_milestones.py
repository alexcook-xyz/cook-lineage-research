import subprocess
import json

milestones = [
    {
        "title": "Milestone 1: Kentucky Line Completeness & Collateral Verification (Gen 1-6)",
        "description": "Solidify all collateral, census, and vital records between Adair/Taylor Counties, KY, and the 1836 migration out of Virginia."
    },
    {
        "title": "Milestone 2: Resolve Generation 7 to 8 Bridge (Pittsylvania Co., VA, 1780-1837)",
        "description": "Close the 75-80% working hypothesis connecting George B (d. 1831) to George Cook Sr. (1835 testator) via restricted Film #007642302 (WB 1:293-294), WKU print marriages, and tax list tracking."
    },
    {
        "title": "Milestone 3: Pre-1780 Southside Piedmont Migration Bridge (1750-1780)",
        "description": "Track the migration of George Cook backward from Pittsylvania across Halifax, Lunenburg, Prince Edward, and Amelia Counties, VA."
    },
    {
        "title": "Milestone 4: Colonial Roots to Immigrant Arrival (Pre-1750)",
        "description": "Trace parentage and transatlantic arrival of the earliest Virginia colonial Cook ancestor through Tidewater patents and British port records."
    }
]

for m in milestones:
    cmd = [
        "gh", "api", "repos/alexcook-xyz/cook-lineage-research/milestones",
        "-X", "POST",
        "-f", f"title={m['title']}",
        "-f", f"description={m['description']}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        data = json.loads(res.stdout)
        print(f"Created milestone #{data['number']}: {data['title']}")
    else:
        print(f"Error creating milestone {m['title']}: {res.stderr}")
