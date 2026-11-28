#!/usr/bin/env python3
"""Build public, machine-readable outputs for a genealogy research repository and check release readiness.

Usage (run from anywhere; REPO defaults to the current git root or directory):
    python3 build_publication.py [REPO]            build exports/ and INDEX.md
    python3 build_publication.py [REPO] --check    verify the repo is ready to publish (exit 1 on errors)
    python3 build_publication.py --self-test       run the built-in tests

Outputs (all generated; never edit by hand):
    exports/people.csv  exports/facts.csv  exports/sources.csv
    exports/sources.csl.json   (CSL-JSON, imports into Zotero and most reference managers)
    exports/pedigree.ged       (GEDCOM 7.0, opens in RootsMagic, Gramps, FamilySearch tools, etc.)
    INDEX.md                   (finding aid: questions, people, confidence)

Privacy: living people (living: true, or born < 100 years ago with no death date) and merged duplicates are
excluded from every output. Links to them are dropped. Only the count is reported.
Uses only the Python standard library.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Reuse the validator's parser. In a research repo both live in tools/; in the skills repo they are siblings.
_here = Path(__file__).resolve().parent
for _cand in (_here, _here.parent.parent / "repo-schema-validate" / "scripts"):
    if (_cand / "validate.py").is_file():
        sys.path.insert(0, str(_cand))
        break
import validate as V  # noqa: E402

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
QUALIFIERS = {"abt": "ABT", "about": "ABT", "bef": "BEF", "before": "BEF", "aft": "AFT", "after": "AFT",
              "cal": "CAL", "est": "EST"}
REQUIRED_ROOT = ["README.md", "LICENSE", "CITATION.cff", "METHODS.md", "ETHICS.md", "CONTRIBUTING.md", "CHANGELOG.md"]
TEXT_CHECKED = ["README.md", "CITATION.cff", "METHODS.md", "ETHICS.md", "CONTRIBUTING.md", "CHANGELOG.md"]
CFF_KEYS = ["cff-version", "message", "title", "authors", "license"]


# ----------------------------------------------------------------------------- loading

def find_root(arg: str | None) -> Path:
    if arg:
        return Path(arg).resolve()
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return Path.cwd()


def load(root: Path, folder: str, prefix: str) -> dict[str, dict]:
    items: dict[str, dict] = {}
    d = root / folder
    if not d.is_dir():
        return items
    for p in sorted(d.glob(f"{prefix}*.md")):
        fm, body = V.parse_frontmatter(p.read_text(encoding="utf-8"))
        if fm is None:
            continue
        fm = dict(fm)
        fm["_body"] = body
        fm["_id"] = p.stem
        items[p.stem] = fm
    return items


def is_living(fm: dict) -> bool:
    if fm.get("living") is True:
        return True
    died = str(fm.get("died", "")).strip()
    m = V.YEAR_RE.search(str(fm.get("born", "")))
    return bool(m) and not died and dt.date.today().year - int(m.group(1)) < 100


def split_people(people: dict[str, dict]) -> tuple[dict[str, dict], list[str]]:
    public, withheld = {}, []
    for pid, fm in people.items():
        if fm.get("merged_into"):
            continue
        (withheld.append(pid) if is_living(fm) else public.__setitem__(pid, fm))
    return public, withheld


def fact_rows(fm: dict) -> list[dict]:
    block = V.section(fm["_body"], "Facts")
    if not block:
        return []
    header, rows = V.table_rows(block)
    out = []
    for r in rows:
        if len(r) >= len(header):
            out.append(dict(zip(header, r)))
    return out


def as_list(v) -> list[str]:
    return v if isinstance(v, list) else ([v] if v else [])


# ----------------------------------------------------------------------------- GEDCOM

def xref(pid: str) -> str:
    return "@" + re.sub(r"[^A-Z0-9_]", "_", pid.upper()) + "@"


def ged_date(raw: str) -> str | None:
    s = str(raw).strip()
    if not s:
        return None
    m = re.fullmatch(r"(?i)(abt|about|bef|before|aft|after|cal|est)?\.?\s*(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", s)
    if m:
        q, y, mo, d = m.groups()
        text = y
        if mo and 1 <= int(mo) <= 12:
            text = f"{MONTHS[int(mo) - 1]} {y}"
            if d:
                text = f"{int(d)} {text}"
        return f"{QUALIFIERS[q.lower()]} {text}" if q else text
    m = re.fullmatch(r"(?i)(abt|about|bef|before|aft|after|cal|est)?\.?\s*(\d{1,2})\s+([A-Za-z]{3})[a-z]*\.?\s+(\d{4})", s)
    if m:
        q, d, mon, y = m.groups()
        if mon.upper() in MONTHS:
            text = f"{int(d)} {mon.upper()} {y}"
            return f"{QUALIFIERS[q.lower()]} {text}" if q else text
    return None


def ged_name(name: str) -> str:
    parts = name.split()
    return f"{' '.join(parts[:-1])} /{parts[-1]}/" if len(parts) > 1 else name


def build_gedcom(public: dict[str, dict]) -> str:
    fams: dict[tuple[str | None, str | None], set[str]] = {}
    for pid, fm in public.items():
        f, m = fm.get("father") or None, fm.get("mother") or None
        f = f if f in public else None
        m = m if m in public else None
        if f or m:
            fams.setdefault((f, m), set()).add(pid)
    for pid, fm in public.items():
        for s in as_list(fm.get("spouses")):
            if s not in public or s == pid:
                continue
            if (pid, s) in fams or (s, pid) in fams:
                continue
            a, b = (s, pid) if public[s].get("sex") == "M" and public[pid].get("sex") != "M" else (pid, s)
            fams.setdefault((a, b), set())
    fam_id = {k: f"@F{i}@" for i, k in enumerate(sorted(fams, key=lambda k: (k[0] or "", k[1] or "")), 1)}
    fams_of: dict[str, list[str]] = {}
    famc_of: dict[str, str] = {}
    for k, kids in fams.items():
        for parent in k:
            if parent:
                fams_of.setdefault(parent, []).append(fam_id[k])
        for c in kids:
            famc_of[c] = fam_id[k]

    used_sources: set[str] = set()
    lines = ["0 HEAD", "1 GEDC", "2 VERS 7.0", "1 SOUR genealogy-agent-skills", "2 VERS 1",
             f"1 DATE {dt.date.today().day} {MONTHS[dt.date.today().month - 1]} {dt.date.today().year}"]
    for pid in sorted(public):
        fm = public[pid]
        lines += [f"0 {xref(pid)} INDI", f"1 NAME {ged_name(str(fm.get('name', pid)))}"]
        sex = str(fm.get("sex", "U"))
        lines.append(f"1 SEX {sex if sex in ('M', 'F', 'U') else 'U'}")
        for tag, dkey, pkey in (("BIRT", "born", "born_place"), ("DEAT", "died", "died_place")):
            d, pl = str(fm.get(dkey, "")).strip(), str(fm.get(pkey, "")).strip()
            if d or pl:
                lines.append(f"1 {tag}")
                gd = ged_date(d)
                if gd:
                    lines.append(f"2 DATE {gd}")
                elif d:
                    lines.append(f"2 NOTE Date as recorded: {d}")
                if pl:
                    lines.append(f"2 PLAC {pl}")
        for fid in fams_of.get(pid, []):
            lines.append(f"1 FAMS {fid}")
        if pid in famc_of:
            lines.append(f"1 FAMC {famc_of[pid]}")
        lines.append(f"1 NOTE Confidence: {fm.get('confidence', 'unknown')}. Evidence and sources: people/{pid}.md")
        for row in fact_rows(fm):
            for s in V.LINK_RE.findall(row.get("sources", "")):
                used_sources.add(s)
        for s in sorted({s for row in fact_rows(fm) for s in V.LINK_RE.findall(row.get("sources", ""))}):
            lines.append(f"1 SOUR {xref(s)}")
    for k in sorted(fams, key=lambda k: fam_id[k]):
        lines.append(f"0 {fam_id[k]} FAM")
        if k[0]:
            lines.append(f"1 HUSB {xref(k[0])}")
        if k[1]:
            lines.append(f"1 WIFE {xref(k[1])}")
        for c in sorted(fams[k]):
            lines.append(f"1 CHIL {xref(c)}")
    for s in sorted(used_sources):
        lines += [f"0 {xref(s)} SOUR", f"1 TITL {s}"]
    lines.append("0 TRLR")
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------- exports and index

CSL_TYPE = {"book": "book", "newspaper": "article-newspaper"}


def write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def build(root: Path) -> dict[str, int]:
    people = load(root, "people", "P-")
    sources = load(root, "sources", "S-")
    public, withheld = split_people(people)
    ex = root / "exports"
    ex.mkdir(exist_ok=True)

    write_csv(ex / "people.csv",
              ["id", "name", "sex", "born", "born_place", "died", "died_place", "father", "mother",
               "spouses", "confidence", "questions"],
              [[pid, fm.get("name", ""), fm.get("sex", ""), fm.get("born", ""), fm.get("born_place", ""),
                fm.get("died", ""), fm.get("died_place", ""),
                fm.get("father", "") if fm.get("father") in public else "",
                fm.get("mother", "") if fm.get("mother") in public else "",
                ";".join(s for s in as_list(fm.get("spouses")) if s in public),
                fm.get("confidence", ""), ";".join(as_list(fm.get("questions")))]
               for pid, fm in sorted(public.items())])

    write_csv(ex / "facts.csv", ["person_id", "fact", "date", "place", "evidence", "sources", "confidence"],
              [[pid, r.get("fact", ""), r.get("date", ""), r.get("place", ""), r.get("evidence", ""),
                ";".join(V.LINK_RE.findall(r.get("sources", ""))), r.get("confidence", "")]
               for pid, fm in sorted(public.items()) for r in fact_rows(fm)])

    write_csv(ex / "sources.csv",
              ["id", "title", "type", "source_class", "repository", "url", "accessed", "citation"],
              [[sid, fm.get("title", ""), fm.get("type", ""), fm.get("source_class", ""),
                fm.get("repository", ""), fm.get("url", ""), fm.get("accessed", ""),
                " ".join((V.section(fm["_body"], "Citation") or "").split())]
               for sid, fm in sorted(sources.items())])

    csl = []
    for sid, fm in sorted(sources.items()):
        item = {"id": sid, "type": CSL_TYPE.get(str(fm.get("type")), "document"), "title": fm.get("title", ""),
                "note": " ".join((V.section(fm["_body"], "Citation") or "").split())}
        if fm.get("repository"):
            item["publisher"] = fm["repository"]
        if fm.get("url"):
            item["URL"] = fm["url"]
        m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(fm.get("accessed", "")))
        if m:
            item["accessed"] = {"date-parts": [[int(x) for x in m.groups()]]}
        csl.append(item)
    (ex / "sources.csl.json").write_text(json.dumps(csl, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    (ex / "pedigree.ged").write_text(build_gedcom(public), encoding="utf-8")
    (root / "INDEX.md").write_text(build_index(root, public, withheld, sources), encoding="utf-8")
    return {"people_public": len(public), "people_withheld": len(withheld), "sources": len(sources)}


def build_index(root: Path, public: dict, withheld: list, sources: dict) -> str:
    out = ["<!-- Generated by tools/build_publication.py. Do not edit by hand. -->", "# Finding aid", ""]
    counts: dict[str, int] = {}
    for fm in public.values():
        counts[str(fm.get("confidence"))] = counts.get(str(fm.get("confidence")), 0) + 1
    out += [f"- **People published:** {len(public)} "
            f"({', '.join(f'{n} {c}' for c, n in sorted(counts.items())) or 'none'})",
            f"- **Withheld as living or recent:** {len(withheld)} (not listed anywhere in this repository's outputs)",
            f"- **Sources:** {len(sources)}",
            "- **Data:** [people.csv](exports/people.csv) · [facts.csv](exports/facts.csv) · "
            "[sources.csv](exports/sources.csv) · [sources.csl.json](exports/sources.csl.json) · "
            "[pedigree.ged](exports/pedigree.ged) (GEDCOM 7.0)",
            "- **How to read confidence grades:** see [METHODS.md](METHODS.md)", "",
            "## Research questions", "",
            "| Question | Title | Status | Review |", "|---|---|---|---|"]
    qdir = root / "questions"
    for q in sorted(p for p in qdir.glob("Q-*") if p.is_dir()) if qdir.is_dir() else []:
        title, status, verdict = q.name, "", ""
        plan = q / "plan.md"
        if plan.is_file():
            fm, body = V.parse_frontmatter(plan.read_text(encoding="utf-8"))
            status = str((fm or {}).get("status", ""))
            h = re.search(r"^#\s+(?:Plan:\s*)?(.+)$", body, re.M)
            title = h.group(1).strip() if h else q.name
        rv = q / "review.md"
        if rv.is_file():
            fm, _ = V.parse_frontmatter(rv.read_text(encoding="utf-8"))
            verdict = str((fm or {}).get("verdict", ""))
        out.append(f"| [{q.name}](questions/{q.name}/) | {title} | {status} | {verdict or 'not reviewed'} |")
    out += ["", "## People", "", "| Name | Born – died | Confidence | Questions |", "|---|---|---|---|"]
    for pid, fm in sorted(public.items(), key=lambda kv: str(kv[1].get("name", kv[0])).lower()):
        span = f"{fm.get('born', '') or '?'} – {fm.get('died', '') or '?'}"
        out.append(f"| [{fm.get('name', pid)}](people/{pid}.md) | {span} | {fm.get('confidence', '')} | "
                   f"{', '.join(as_list(fm.get('questions')))} |")
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------- readiness check

def check(root: Path) -> list[str]:
    errors: list[str] = []
    for f in REQUIRED_ROOT:
        if not (root / f).is_file():
            errors.append(f"missing {f}")
    for f in TEXT_CHECKED:
        p = root / f
        if p.is_file():
            t = p.read_text(encoding="utf-8")
            if "{{" in t:
                errors.append(f"{f}: unresolved placeholder {{{{...}}}}")
            if re.search(r"\bTODO\b", t):
                errors.append(f"{f}: contains TODO")
    cff = root / "CITATION.cff"
    if cff.is_file():
        t = cff.read_text(encoding="utf-8")
        for k in CFF_KEYS:
            if not re.search(rf"^{re.escape(k)}\s*:", t, re.M):
                errors.append(f"CITATION.cff: missing key '{k}'")
    lic = root / "LICENSE"
    if lic.is_file() and len(lic.read_text(encoding="utf-8").strip()) < 200:
        errors.append("LICENSE: looks empty or truncated; use the official license text")

    rep = V.validate(root)
    errors += [e.replace("ERROR   ", "validator: ", 1) for e in rep.errors]

    media = root / "media"
    if media.is_dir() and any(p.is_file() and p.name not in {".gitkeep", "RIGHTS.md"} for p in media.rglob("*")):
        if not (media / "RIGHTS.md").is_file():
            errors.append("media/ has files but no media/RIGHTS.md stating the right to redistribute each one")

    ex = root / "exports"
    for f in ("people.csv", "facts.csv", "sources.csv", "sources.csl.json", "pedigree.ged"):
        if not (ex / f).is_file():
            errors.append(f"exports/{f} missing; run build_publication.py")
    if not (root / "INDEX.md").is_file():
        errors.append("INDEX.md missing; run build_publication.py")

    people = load(root, "people", "P-")
    _, withheld = split_people(people)
    if ex.is_dir():
        blobs = {p.name: p.read_text(encoding="utf-8", errors="replace") for p in ex.iterdir() if p.is_file()}
        blobs["INDEX.md"] = (root / "INDEX.md").read_text(encoding="utf-8") if (root / "INDEX.md").is_file() else ""
        for pid in withheld:
            for name, text in blobs.items():
                if pid in text or xref(pid) in text or str(people[pid].get("name", "\0")) in text:
                    errors.append(f"{name}: contains withheld living/recent person {pid}; rebuild exports")
    return errors


# ----------------------------------------------------------------------------- self-test

def self_test() -> int:
    failures: list[str] = []

    def ok(name: str, cond: bool) -> None:
        print(f"  {'ok  ' if cond else 'FAIL'} {name}")
        if not cond:
            failures.append(name)

    def w(root: Path, rel: str, text: str) -> None:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    print("build_publication.py self-test")
    root = Path(tempfile.mkdtemp(prefix="gps-publish-"))
    w(root, "sources/S-a.md", V.GOOD_SOURCE.replace("S-1850-census-x", "S-a"))
    person = lambda pid, name, extra: (f"---\nid: {pid}\nname: {name}\nsex: M\nliving: false\nconfidence: probable\n"
                                       f"{extra}---\n## Facts\n\n| Fact | Date | Place | Evidence | Sources | Confidence |\n"
                                       f"|---|---|---|---|---|---|\n| Birth | 1792 | VA | indirect | [[S-a]] | probable |\n")
    w(root, "people/P-father-1765.md", person("P-father-1765", "William Cook", "born: 1765\ndied: 1830\n"))
    w(root, "people/P-john-1792.md", person("P-john-1792", "John Cook", "born: abt 1792\ndied: 1861-03-04\nfather: P-father-1765\n"))
    w(root, "people/P-alive.md", person("P-alive", "Zed Living", "born: 2001\nfather: P-john-1792\n").replace("living: false", "living: true"))
    w(root, "questions/Q-1/plan.md", "---\nquestion: Q-1\nstatus: resolved\n---\n# Plan: Who was the father of John Cook?\n")
    stats = build(root)
    ged = (root / "exports/pedigree.ged").read_text(encoding="utf-8")
    ok("counts: 2 public, 1 withheld", stats["people_public"] == 2 and stats["people_withheld"] == 1)
    ok("GEDCOM has header and trailer", ged.startswith("0 HEAD") and ged.rstrip().endswith("0 TRLR"))
    ok("GEDCOM 7.0 declared", "2 VERS 7.0" in ged)
    ok("GEDCOM links child to parents' family", "1 CHIL @P_JOHN_1792@" in ged and "1 HUSB @P_FATHER_1765@" in ged)
    ok("GEDCOM normalizes dates", "2 DATE 4 MAR 1861" in ged and "2 DATE ABT 1792" in ged)
    ok("GEDCOM name has surname slashes", "1 NAME John /Cook/" in ged)
    outputs = "".join(p.read_text(encoding="utf-8") for p in (root / "exports").iterdir()) + (root / "INDEX.md").read_text(encoding="utf-8")
    ok("living person absent from all outputs", "Zed" not in outputs and "P-alive" not in outputs and "P_ALIVE" not in outputs)
    ok("CSL-JSON parses", isinstance(json.loads((root / "exports/sources.csl.json").read_text()), list))
    ok("INDEX lists the question title", "Who was the father of John Cook?" in (root / "INDEX.md").read_text())
    errs = check(root)
    ok("check fails when publication files are missing", any("missing README.md" in e for e in errs))
    for f in REQUIRED_ROOT:
        w(root, f, "x" * 300 if f == "LICENSE" else "content\n")
    w(root, "CITATION.cff", "cff-version: 1.2.0\nmessage: cite\ntitle: t\nauthors:\n  - name: a\nlicense: CC-BY-4.0\n")
    ok("check passes when complete", check(root) == [])
    w(root, "README.md", "Name: {{AUTHOR}}\n")
    ok("check catches placeholders", any("placeholder" in e for e in check(root)))
    w(root, "README.md", "ok\n")
    w(root, "exports/people.csv", "id\nP-alive\n")
    ok("check catches a living person in exports", any("withheld" in e for e in check(root)))
    print("PASS" if not failures else f"FAILED: {failures}")
    return 0 if not failures else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("-")]
    root = find_root(args[0] if args else None)
    if "--check" in argv:
        errs = check(root)
        for e in errs:
            print("ERROR", e)
        print(f"\n{len(errs)} problem(s). {'Ready to publish.' if not errs else 'Not ready to publish.'}")
        return 1 if errs else 0
    stats = build(root)
    print(f"Built exports/ and INDEX.md in {root}: {stats['people_public']} people published, "
          f"{stats['people_withheld']} withheld (living/recent), {stats['sources']} sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
