#!/usr/bin/env python3
"""Validate a genealogy research repository against CONVENTIONS.md.

Usage:
    python3 validate.py [REPO_PATH]       validate a repository (default: .)
    python3 validate.py --self-test       run the built-in tests

Exit code 0 when there are no errors (warnings are allowed), 1 otherwise.
Uses only the Python standard library.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
import tempfile
from pathlib import Path

CONFIDENCE = {"proven", "probable", "possible", "tradition", "disproven"}
EVIDENCE = {"direct", "indirect", "negative"}
SEX = {"M", "F", "U"}
SOURCE_TYPES = {
    "census", "vital", "church", "probate", "land", "court", "tax", "military",
    "immigration", "newspaper", "directory", "dna", "book", "oral", "other",
}
SOURCE_CLASS = {"original", "derivative", "authored"}
QUESTION_STATUS = {"open", "in-progress", "resolved", "stalled"}
QUESTION_FILES = ("plan.md", "log.md", "analysis.md", "proof.md", "review.md", "pipeline.md", "second-opinion.md")

PERSON_KEYS = {"id", "name", "sex", "living", "confidence"}
SOURCE_KEYS = {"id", "title", "type", "source_class", "accessed"}

LINK_RE = re.compile(r"\[\[([A-Za-z0-9][A-Za-z0-9._-]*)\]\]")
PRIVACY_RE = re.compile(r"\b(kit\s*(number|no\.?|#|id)\s*[:=]?\s*[A-Z]{0,3}\d{4,})", re.I)
MATCH_NAME_RE = re.compile(r"\bmatch(?:ed)?\s+name\s*:", re.I)
YEAR_RE = re.compile(r"\b(1[0-9]{3}|20[0-9]{2})\b")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, path: Path | str, msg: str) -> None:
        self.errors.append(f"ERROR   {path}: {msg}")

    def warn(self, path: Path | str, msg: str) -> None:
        self.warnings.append(f"WARNING {path}: {msg}")


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str]:
    """Parse flat YAML frontmatter. Returns (data, body); data is None if absent."""
    if not text.startswith("---"):
        return None, text
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    data: dict[str, object] = {}
    for raw in lines[1:end]:
        line = raw.split(" #", 1)[0].rstrip() if " #" in raw else raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()] if inner else []
        elif value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value.strip("'\"")
    return data, "\n".join(lines[end + 1:])


def section(body: str, heading: str) -> str | None:
    """Return the text under '## heading' up to the next '## ' heading."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", body, re.M)
    if not m:
        return None
    rest = body[m.end():]
    n = re.search(r"^##\s+", rest, re.M)
    return rest[: n.start()] if n else rest


def table_rows(block: str) -> tuple[list[str], list[list[str]]]:
    rows = [ln.strip() for ln in block.splitlines() if ln.strip().startswith("|")]
    if len(rows) < 2:
        return [], []
    cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
    header = [h.lower() for h in cells(rows[0])]
    body_rows = [cells(r) for r in rows[2:]]
    return header, body_rows


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(root: Path) -> Report:
    rep = Report()
    people_dir, sources_dir, questions_dir = root / "people", root / "sources", root / "questions"

    people_ids = {p.stem for p in people_dir.glob("P-*.md")} if people_dir.is_dir() else set()
    source_ids = {p.stem for p in sources_dir.glob("S-*.md")} if sources_dir.is_dir() else set()
    question_ids = {p.name for p in questions_dir.glob("Q-*") if p.is_dir()} if questions_dir.is_dir() else set()
    all_ids = people_ids | source_ids

    # Which questions have a passing review and a proof.
    reviewed_pass: set[str] = set()
    for q in sorted(question_ids):
        qdir = questions_dir / q
        rv = qdir / "review.md"
        pf = qdir / "proof.md"
        if rv.is_file():
            fm, _ = parse_frontmatter(read(rv))
            if fm and fm.get("verdict") == "pass" and pf.is_file():
                reviewed_pass.add(q)

    # Sources whose Notes say the transcription came from Muse and has not been checked against the image.
    unverified_sources: set[str] = set()      # never checked against the image
    screenshot_only_sources: set[str] = set()  # checked against a screenshot only, not the full image
    for sid in source_ids:
        body_txt = read(sources_dir / f"{sid}.md")
        if "Unverified Muse transcription" in body_txt:
            unverified_sources.add(sid)
        if "Checked against a screenshot only" in body_txt:
            screenshot_only_sources.add(sid)

    # ---- sources
    for sid in sorted(source_ids):
        path = sources_dir / f"{sid}.md"
        rel = path.relative_to(root)
        text = read(path)
        fm, body = parse_frontmatter(text)
        if fm is None:
            rep.error(rel, "missing frontmatter")
            continue
        for k in sorted(SOURCE_KEYS):
            if not fm.get(k):
                rep.error(rel, f"missing frontmatter key '{k}'")
        if fm.get("id") and fm["id"] != sid:
            rep.error(rel, f"id '{fm['id']}' does not match file name '{sid}'")
        if fm.get("type") and fm["type"] not in SOURCE_TYPES:
            rep.error(rel, f"type '{fm['type']}' is not one of {sorted(SOURCE_TYPES)}")
        if fm.get("source_class") and fm["source_class"] not in SOURCE_CLASS:
            rep.error(rel, f"source_class '{fm['source_class']}' is not one of {sorted(SOURCE_CLASS)}")
        cit = section(body, "Citation")
        if cit is None or len(cit.strip()) < 20:
            rep.error(rel, "missing or empty '## Citation' section")
        img = fm.get("image")
        if isinstance(img, str) and img and not (root / img).exists():
            rep.warn(rel, f"image '{img}' not found")
        _privacy(rep, rel, text)
        _links(rep, rel, text, all_ids)

    # ---- people
    for pid in sorted(people_ids):
        path = people_dir / f"{pid}.md"
        rel = path.relative_to(root)
        text = read(path)
        fm, body = parse_frontmatter(text)
        if fm is None:
            rep.error(rel, "missing frontmatter")
            continue
        for k in sorted(PERSON_KEYS):
            if fm.get(k) in (None, ""):
                rep.error(rel, f"missing frontmatter key '{k}'")
        if fm.get("id") and fm["id"] != pid:
            rep.error(rel, f"id '{fm['id']}' does not match file name '{pid}'")
        if fm.get("sex") and fm["sex"] not in SEX:
            rep.error(rel, f"sex '{fm['sex']}' is not M, F, or U")
        if fm.get("confidence") and fm["confidence"] not in CONFIDENCE:
            rep.error(rel, f"confidence '{fm['confidence']}' is not one of {sorted(CONFIDENCE)}")
        if "living" in fm and not isinstance(fm["living"], bool):
            rep.error(rel, "living must be true or false")

        for key in ("father", "mother", "merged_into"):
            val = fm.get(key)
            if isinstance(val, str) and val and val not in people_ids:
                rep.error(rel, f"{key} '{val}' does not exist in people/")
        spouses = fm.get("spouses")
        if isinstance(spouses, list):
            for s in spouses:
                if s not in people_ids:
                    rep.error(rel, f"spouse '{s}' does not exist in people/")
        qs = fm.get("questions")
        qlist = qs if isinstance(qs, list) else []
        for q in qlist:
            if q not in question_ids:
                rep.error(rel, f"question '{q}' has no folder in questions/")

        merged = bool(fm.get("merged_into"))
        facts = section(body, "Facts")
        if not merged:
            if facts is None:
                rep.error(rel, "missing '## Facts' table")
            else:
                header, rows = table_rows(facts)
                need = ["fact", "evidence", "sources", "confidence"]
                if not header or any(n not in header for n in need):
                    rep.error(rel, f"Facts table needs columns including {need}")
                else:
                    ix = {n: header.index(n) for n in need}
                    if not rows:
                        rep.error(rel, "Facts table has no rows")
                    for r in rows:
                        if len(r) < len(header):
                            rep.error(rel, f"Facts row has too few cells: {r}")
                            continue
                        label = r[ix["fact"]] or "(blank)"
                        conf = r[ix["confidence"]].lower()
                        ev = r[ix["evidence"]].lower()
                        links = LINK_RE.findall(r[ix["sources"]])
                        if conf not in CONFIDENCE:
                            rep.error(rel, f"fact '{label}': confidence '{conf}' invalid")
                        if ev and ev not in EVIDENCE:
                            rep.error(rel, f"fact '{label}': evidence '{ev}' invalid")
                        if not links and conf != "tradition":
                            rep.error(rel, f"fact '{label}': no [[S-...]] source (only 'tradition' may lack one)")
                        for lk in links:
                            if lk not in source_ids:
                                rep.error(rel, f"fact '{label}': source '{lk}' does not exist in sources/")
                        if conf == "proven" and any(lk in unverified_sources or lk in screenshot_only_sources for lk in links):
                            rep.error(rel, f"fact '{label}' is 'proven' but cites a Muse source that is unverified or checked against a "
                                           "screenshot only; verify it against the full image (or a human reader) and replace the Notes marker")
                        elif conf == "probable" and links and all(lk in unverified_sources for lk in links):
                            rep.warn(rel, f"fact '{label}' is 'probable' but rests only on unverified Muse transcriptions; "
                                          "grade it 'possible' or add an independent source")
                        if conf == "proven" and not (set(qlist) & reviewed_pass):
                            rep.error(
                                rel,
                                f"fact '{label}' is 'proven' but none of this person's questions "
                                "has proof.md plus a review.md with verdict: pass",
                            )
        if fm.get("confidence") == "proven" and not (set(qlist) & reviewed_pass):
            rep.error(rel, "person confidence is 'proven' without a passing reviewed question")

        # privacy
        born = str(fm.get("born", ""))
        died = str(fm.get("died", ""))
        year = YEAR_RE.search(born)
        recent_no_death = bool(year) and (dt.date.today().year - int(year.group(1)) < 100) and not died.strip()
        if fm.get("living") is True or recent_no_death:
            rep.warn(rel, "treated as a living person: keep this repository private and details minimal")
        _privacy(rep, rel, text)
        _links(rep, rel, text, all_ids)

    # ---- questions
    for q in sorted(question_ids):
        qdir = questions_dir / q
        for fname in QUESTION_FILES:
            f = qdir / fname
            if not f.is_file():
                continue
            rel = f.relative_to(root)
            text = read(f)
            fm, _ = parse_frontmatter(text)
            if fm is None:
                rep.error(rel, "missing frontmatter")
                continue
            if fm.get("question") != q:
                rep.error(rel, f"question '{fm.get('question')}' does not match folder '{q}'")
            if fm.get("status") not in QUESTION_STATUS:
                rep.error(rel, f"status '{fm.get('status')}' is not one of {sorted(QUESTION_STATUS)}")
            if fname == "review.md" and fm.get("verdict") not in {"pass", "fail"}:
                rep.error(rel, "review.md needs verdict: pass or fail")
            _privacy(rep, rel, text)
            _links(rep, rel, text, all_ids)
        mdir = qdir / "muse"
        if mdir.is_dir():
            for f in sorted(mdir.glob("*.md")):
                rel = f.relative_to(root)
                text = read(f)
                _privacy(rep, rel, text)
                _links(rep, rel, text, all_ids)
        if not (qdir / "plan.md").is_file():
            rep.error(qdir.relative_to(root), "question folder has no plan.md")
        if (qdir / "review.md").is_file() and not (qdir / "proof.md").is_file():
            rep.warn(qdir.relative_to(root), "review.md exists without proof.md")

    return rep


def _links(rep: Report, rel: Path, text: str, all_ids: set[str]) -> None:
    for lk in sorted(set(LINK_RE.findall(text))):
        if lk.startswith(("P-", "S-")) and lk not in all_ids:
            rep.error(rel, f"broken link [[{lk}]]")


def _privacy(rep: Report, rel: Path, text: str) -> None:
    if PRIVACY_RE.search(text):
        rep.error(rel, "looks like a DNA kit number; never store kit identifiers")
    if MATCH_NAME_RE.search(text):
        rep.error(rel, "looks like a DNA match name; refer to matches by local code only")


# --------------------------------------------------------------------------- self-test

GOOD_SOURCE = """---
id: S-1850-census-x
title: 1850 U.S. census, X County, population schedule, p. 1
type: census
source_class: derivative
accessed: 2026-11-27
---
## Citation
1850 U.S. census, X County, Virginia, population schedule, p. 1, dwelling 1, John Cook.

## Transcription
John Cook 58 M farmer
"""

GOOD_PERSON = """---
id: P-john-cook-1792
name: John Cook
sex: M
born: abt 1792
died: 1861
living: false
confidence: probable
questions: [Q-1]
---
## Facts

| Fact | Date | Place | Evidence | Sources | Confidence |
|---|---|---|---|---|---|
| Birth | abt 1792 | Virginia | indirect | [[S-1850-census-x]] | probable |
"""

PLAN = "---\nquestion: Q-1\nstatus: open\n---\n# Plan\n"


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def self_test() -> int:
    failures: list[str] = []

    def check(name: str, ok: bool) -> None:
        if not ok:
            failures.append(name)
        print(f"  {'ok  ' if ok else 'FAIL'} {name}")

    def build(mutate=None) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="gps-validate-"))
        _write(tmp, "sources/S-1850-census-x.md", GOOD_SOURCE)
        _write(tmp, "people/P-john-cook-1792.md", GOOD_PERSON)
        _write(tmp, "questions/Q-1/plan.md", PLAN)
        if mutate:
            mutate(tmp)
        return tmp

    def has(rep: Report, needle: str) -> bool:
        return any(needle in e for e in rep.errors)

    print("validate.py self-test")
    rep = validate(build())
    check("valid repo has no errors", not rep.errors)

    rep = validate(build(lambda t: _write(t, "people/P-john-cook-1792.md",
                                          GOOD_PERSON.replace("[[S-1850-census-x]]", ""))))
    check("fact without source is an error", has(rep, "no [[S-...]] source"))

    rep = validate(build(lambda t: _write(t, "people/P-john-cook-1792.md",
                                          GOOD_PERSON.replace("[[S-1850-census-x]]", "[[S-missing]]"))))
    check("link to missing source is an error", has(rep, "does not exist in sources/"))

    rep = validate(build(lambda t: _write(t, "people/P-john-cook-1792.md",
                                          GOOD_PERSON.replace("| probable |", "| tradition |").replace("[[S-1850-census-x]]", ""))))
    check("tradition fact may lack a source", not has(rep, "no [[S-...]] source"))

    rep = validate(build(lambda t: _write(t, "people/P-john-cook-1792.md",
                                          GOOD_PERSON.replace("| probable |", "| proven |"))))
    check("proven without review is an error", has(rep, "is 'proven'"))

    def add_review(t: Path) -> None:
        _write(t, "people/P-john-cook-1792.md", GOOD_PERSON.replace("| probable |", "| proven |"))
        _write(t, "questions/Q-1/proof.md", "---\nquestion: Q-1\nstatus: resolved\n---\n# Proof\n")
        _write(t, "questions/Q-1/review.md",
               "---\nquestion: Q-1\nstatus: resolved\nverdict: pass\nreviewer: adversarial-reviewer\n---\n# Review\n")
    rep = validate(build(add_review))
    check("proven with proof and passing review is accepted", not has(rep, "is 'proven'"))

    rep = validate(build(lambda t: _write(t, "people/P-bad-name.md", GOOD_PERSON)))
    check("id/file name mismatch is an error", has(rep, "does not match file name"))

    rep = validate(build(lambda t: _write(t, "sources/S-1850-census-x.md", GOOD_SOURCE.replace("type: census", "type: gossip"))))
    check("invalid source type is an error", has(rep, "type 'gossip'"))

    rep = validate(build(lambda t: _write(t, "sources/S-1850-census-x.md", GOOD_SOURCE.replace("## Citation", "## Cite"))))
    check("missing Citation section is an error", has(rep, "Citation"))

    rep = validate(build(lambda t: _write(t, "questions/Q-1/log.md",
                                          "---\nquestion: Q-1\nstatus: open\n---\nKit number: A123456\n")))
    check("DNA kit number is an error", has(rep, "kit number"))

    rep = validate(build(lambda t: _write(t, "questions/Q-1/log.md",
                                          "---\nquestion: Q-1\nstatus: open\n---\nSee [[P-nobody]]\n")))
    check("broken person link is an error", has(rep, "broken link"))

    rep = validate(build(lambda t: _write(t, "people/P-john-cook-1792.md", GOOD_PERSON.replace("living: false", "living: true"))))
    check("living person gives a warning", any("living" in w for w in rep.warnings))

    rep = validate(build(lambda t: _write(t, "questions/Q-2/log.md", "---\nquestion: Q-2\nstatus: open\n---\n")))
    check("question folder without plan is an error", has(rep, "no plan.md"))

    unverified_src = GOOD_SOURCE + "\n## Notes\nUnverified Muse transcription. Verify against the image.\n"

    def proven_unverified(t: Path) -> None:
        add_review(t)
        _write(t, "sources/S-1850-census-x.md", unverified_src)
    rep = validate(build(proven_unverified))
    check("proven fact on an unverified Muse source is an error", has(rep, "unverified or checked"))

    shot_src = GOOD_SOURCE + "\n## Notes\nChecked against a screenshot only by evidence-analyst, 2026-11-27.\n"

    def proven_shot(t: Path) -> None:
        add_review(t)
        _write(t, "sources/S-1850-census-x.md", shot_src)
    rep = validate(build(proven_shot))
    check("proven fact on a screenshot-only Muse source is an error", has(rep, "screenshot only"))

    rep = validate(build(lambda t: _write(t, "sources/S-1850-census-x.md", unverified_src)))
    check("probable fact resting only on unverified Muse sources warns", any("Muse" in w for w in rep.warnings) and not rep.errors)

    rep = validate(build(lambda t: _write(t, "questions/Q-1/muse/M-1.request.md", "Kit number: A123456\n")))
    check("Muse request files are scanned for kit numbers", has(rep, "kit number"))

    print("PASS" if not failures else f"FAILED: {failures}")
    return 0 if not failures else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("-")]
    root = Path(args[0] if args else ".").resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    rep = validate(root)
    for line in rep.warnings + rep.errors:
        print(line)
    print(f"\n{len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
