#!/usr/bin/env python3
"""Evaluate the mechanical gates of the research pipeline for one question.

Usage:
    python3 pipeline_check.py REPO Q-12 [--through N] [--record]
    python3 pipeline_check.py --self-test

    --through N   check stages 0..N (default 9). Run `--through K` before starting stage K+1.
    --record      write the results into questions/Q-12/pipeline.md (a generated 'Gate log' block)

Stages: 0 repo, 1 plan, 2 search, 3 ingest, 4 analysis, 5 proof, 6 review, 7 validate, 8 knowledge, 9 close.
Exit code 0 = every checked gate passed. Warnings never fail a gate. Standard library only.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import tempfile
from pathlib import Path

_here = Path(__file__).resolve().parent
for _cand in (_here, _here.parent.parent / "repo-schema-validate" / "scripts"):
    if (_cand / "validate.py").is_file():
        sys.path.insert(0, str(_cand))
        break
import validate as V  # noqa: E402

STAGES = ["repo", "plan", "search", "ingest", "analysis", "proof", "review", "validate", "knowledge", "close"]
SELF_REVIEWERS = {"evidence-analyst", "research-lead", "lead", "analyst", "claude", "main", ""}
PLAN_HEADINGS = ["Objective", "Hypotheses", "Record groups", "Done when"]


class Gate:
    def __init__(self, stage: int, name: str, ok: bool, detail: str, warn: bool = False) -> None:
        self.stage, self.name, self.ok, self.detail, self.warn = stage, name, ok, detail, warn

    def label(self) -> str:
        return "PASS" if self.ok and not self.warn else ("WARN" if self.ok else "FAIL")


def fm_of(path: Path) -> dict:
    fm, _ = V.parse_frontmatter(path.read_text(encoding="utf-8"))
    return fm or {}


def has_heading(text: str, name: str) -> bool:
    return bool(re.search(rf"^#{{1,3}}\s*{re.escape(name)}\b", text, re.M | re.I))


def evaluate(repo: Path, q: str, through: int = 9) -> list[Gate]:
    g: list[Gate] = []
    qdir = repo / "questions" / q

    # 0 repo
    is_skills = (repo / ".claude-plugin" / "plugin.json").is_file() and (repo / "CONVENTIONS.md").is_file() and (repo / "skills").is_dir()
    init = all((repo / d).is_dir() for d in ("people", "sources", "questions"))
    g.append(Gate(0, "research repo", init and not is_skills and qdir.is_dir(),
                  "skills repo: research data never goes here" if is_skills else
                  "not an initialized research repo (run research-repo-init)" if not init else
                  f"{q} has no folder under questions/" if not qdir.is_dir() else "initialized; question folder exists"))
    if through < 1 or not qdir.is_dir():
        return g

    # 1 plan
    plan = qdir / "plan.md"
    if not plan.is_file():
        g.append(Gate(1, "plan", False, "questions/%s/plan.md is missing" % q))
    else:
        text = plan.read_text(encoding="utf-8")
        miss = [h for h in PLAN_HEADINGS if not has_heading(text, h)]
        fm = fm_of(plan)
        bad = fm.get("question") != q or fm.get("status") not in V.QUESTION_STATUS
        g.append(Gate(1, "plan", not miss and not bad,
                      f"plan.md lacks sections {miss}" if miss else "plan.md frontmatter invalid" if bad else "plan has objective, hypotheses, record groups, done-when"))
    if through < 2:
        return g

    # 2 search
    log = qdir / "log.md"
    if not log.is_file():
        g.append(Gate(2, "search log", False, "log.md is missing: no search is logged"))
    else:
        t = log.read_text(encoding="utf-8")
        entries = re.split(r"^###\s+", t, flags=re.M)[1:]
        no_result = [i + 1 for i, e in enumerate(entries) if not re.search(r"\*\*Result:\*\*", e)]
        g.append(Gate(2, "search log", bool(entries) and not no_result,
                      "log.md has no entries" if not entries else f"log entries without a Result field: {no_result}" if no_result else f"{len(entries)} logged search(es)"))
        rows = 0
        if plan.is_file():
            block = V.section(plan.read_text(encoding="utf-8"), "Record groups and search order") or V.section(plan.read_text(encoding="utf-8"), "Record groups") or ""
            rows = len(V.table_rows(block)[1])
        if rows and len(entries) < rows:
            g.append(Gate(2, "plan coverage", True, f"plan lists {rows} record group(s) but only {len(entries)} log entr(y/ies): confirm the rest are covered or justified", warn=True))
    if through < 3:
        return g

    # 3 ingest
    muse = qdir / "muse"
    pending, noresult = [], []
    if muse.is_dir():
        for f in sorted(muse.glob("M-*.request.md")):
            fm = fm_of(f)
            if fm.get("status") in {"waiting", "received"}:
                pending.append(f"{fm.get('request', f.name)} ({fm.get('status')})")
            elif fm.get("status") == "ingested" and not fm.get("result"):
                noresult.append(fm.get("request", f.name))
    g.append(Gate(3, "muse requests ingested", not pending and not noresult,
                  f"Muse requests not yet ingested: {pending}" if pending else f"ingested requests without a result: path {noresult}" if noresult else "no pending Muse requests"))
    if through < 4:
        return g

    # 4 analysis
    an = qdir / "analysis.md"
    if not an.is_file():
        g.append(Gate(4, "analysis", False, "analysis.md is missing"))
    else:
        t = an.read_text(encoding="utf-8")
        ok = len(t.strip()) > 200 and has_heading(t, "Conflicts")
        g.append(Gate(4, "analysis", ok, "analysis.md needs content and a '## Conflicts' section (say 'none' if there are none)" if not ok else "analysis with conflicts section"))
    if through < 5:
        return g

    # 5 proof
    stalled = plan.is_file() and fm_of(plan).get("status") == "stalled"
    proof = qdir / "proof.md"
    if stalled:
        t = an.read_text(encoding="utf-8") if an.is_file() else ""
        g.append(Gate(5, "proof", bool(re.search(r"(?i)\b(settle|would answer|next record)\b", t)),
                      "stalled: analysis.md must name the record that would settle the question" if not re.search(r"(?i)\b(settle|would answer|next record)\b", t) else "stalled; the record that would settle it is named"))
    elif not proof.is_file():
        g.append(Gate(5, "proof", False, "proof.md is missing (or mark the question stalled and say what would settle it)"))
    else:
        fm = fm_of(proof)
        g.append(Gate(5, "proof", fm.get("conclusion_confidence") in {"proven", "probable", "possible"}, "proof.md needs conclusion_confidence: proven | probable | possible"
                      if fm.get("conclusion_confidence") not in {"proven", "probable", "possible"} else f"proof written ({fm.get('conclusion_confidence')})"))
    if through < 6:
        return g

    # 6 review
    needs_review = proof.is_file() and fm_of(proof).get("conclusion_confidence") == "proven"
    rv = qdir / "review.md"
    if not needs_review:
        g.append(Gate(6, "review", True, "no `proven` claim, so no review is required"))
    elif not rv.is_file():
        g.append(Gate(6, "review", False, "the proof claims `proven` but review.md is missing"))
    else:
        fm = fm_of(rv)
        reviewer = str(fm.get("reviewer", "")).strip().lower()
        ok = fm.get("verdict") == "pass" and reviewer not in SELF_REVIEWERS
        g.append(Gate(6, "review", ok,
                      f"review verdict is '{fm.get('verdict')}', not pass" if fm.get("verdict") != "pass" else
                      f"reviewer '{reviewer or '(blank)'}' is not independent of the analysis; the adversarial-reviewer agent or a human must review" if reviewer in SELF_REVIEWERS
                      else f"independent review passed ({reviewer})"))
    # 6b optional second opinion (a different model family), required when the plan asks for it
    if needs_review and str(fm_of(plan).get("second_opinion", "")).lower() == "true":
        so = qdir / "second-opinion.md"
        if not so.is_file():
            g.append(Gate(6, "second opinion", False, "plan.md sets second_opinion: true but second-opinion.md is missing (skill second-opinion)"))
        else:
            fm = fm_of(so)
            problems = []
            if fm.get("verdict") != "pass":
                problems.append(f"verdict is '{fm.get('verdict')}', not pass")
            if not str(fm.get("model", "")).strip():
                problems.append("no model recorded")
            raw = str(fm.get("raw", "")).strip()
            note = ""
            if raw and (repo / raw).is_file():
                try:
                    data = json.loads((repo / raw).read_text(encoding="utf-8"))
                    so_out = data.get("structured_output") or {}
                    if data.get("status") != "SUCCESS" or so_out.get("verdict") not in {"pass", "fail"}:
                        problems.append("the raw agy reply is not a successful structured review")
                    elif so_out["verdict"] == "fail" and fm.get("verdict") == "pass":
                        note = " (the model said fail; you recorded pass after checking its findings: make sure the confirmed findings are resolved)"
                except json.JSONDecodeError:
                    problems.append("the raw agy reply is not valid JSON")
            elif raw:
                note = " (raw reply is not on this machine, so it could not be re-checked)"
            g.append(Gate(6, "second opinion", not problems, "; ".join(problems) if problems else f"second opinion passed ({fm.get('model')}){note}", warn=bool(note) and not problems))
    if through < 7:
        return g

    # 7 validate
    rep = V.validate(repo)
    g.append(Gate(7, "validator", not rep.errors, f"{len(rep.errors)} validator error(s): {rep.errors[0][:100]}" if rep.errors else f"validator clean ({len(rep.warnings)} warning(s))"))
    if through < 8:
        return g

    # 8 knowledge
    pl = qdir / "pipeline.md"
    k = str(fm_of(pl).get("knowledge", "")).strip() if pl.is_file() else ""
    g.append(Gate(8, "knowledge capture", bool(k), "pipeline.md needs `knowledge: none` or `knowledge: <PR URL>` (skill knowledge-capture)" if not k else f"knowledge: {k}"))
    if through < 9:
        return g

    # 9 close
    st = fm_of(plan).get("status") if plan.is_file() else ""
    g.append(Gate(9, "close", st in {"resolved", "stalled"}, f"plan.md status is '{st}'; set resolved or stalled to close" if st not in {"resolved", "stalled"} else f"question {st}"))
    return g


def render(gates: list[Gate]) -> str:
    return "\n".join(f"{x.label():5} stage {x.stage} {STAGES[x.stage]:<10} {x.name}: {x.detail}" for x in gates)


def record(repo: Path, q: str, gates: list[Gate]) -> Path:
    pl = repo / "questions" / q / "pipeline.md"
    today = dt.date.today().isoformat()
    block = ["<!-- gates:start -->", "## Gate log (generated by pipeline_check.py)", "",
             f"Last run {today}.", "", "| Stage | Gate | Result | Detail |", "|---|---|---|---|"]
    block += [f"| {x.stage} {STAGES[x.stage]} | {x.name} | {x.label()} | {x.detail.replace('|', '/')} |" for x in gates]
    block.append("<!-- gates:end -->")
    new = "\n".join(block)
    if pl.is_file():
        t = pl.read_text(encoding="utf-8")
        if "<!-- gates:start -->" in t:
            t = re.sub(r"<!-- gates:start -->.*?<!-- gates:end -->", lambda m: new, t, flags=re.S)
        else:
            t = t.rstrip("\n") + "\n\n" + new + "\n"
    else:
        t = f"---\nquestion: {q}\nstatus: open\nknowledge:\n---\n# Pipeline: {q}\n\n{new}\n"
    pl.write_text(t, encoding="utf-8")
    return pl


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

    PLAN = ("---\nquestion: Q-1\nstatus: open\n---\n# Plan: who?\n## Objective\nx\n## Hypotheses\n1. a\n"
            "## Record groups and search order\n| # | Record group | Repository |\n|---|---|---|\n| 1 | deeds | LVA |\n## Done when\nx\n")
    LOG = "---\nquestion: Q-1\nstatus: open\n---\n### 2026-11-27 — LVA: deeds\n- **Result:** found\n"
    AN = "---\nquestion: Q-1\nstatus: open\n---\n# Analysis\n" + "text " * 60 + "\n## Conflicts\nnone\n"
    PROOF = "---\nquestion: Q-1\nstatus: resolved\nconclusion_confidence: {c}\n---\n# Proof\n"
    REVIEW = "---\nquestion: Q-1\nstatus: resolved\nverdict: {v}\nreviewer: {r}\n---\n# Review\n"

    def repo(stage_files: dict[str, str] | None = None) -> Path:
        r = Path(tempfile.mkdtemp(prefix="gps-pipe-"))
        w(r, "sources/S-1850-census-x.md", V.GOOD_SOURCE)
        w(r, "people/P-john-cook-1792.md", V.GOOD_PERSON)
        w(r, "questions/Q-1/plan.md", PLAN)
        for k, v in (stage_files or {}).items():
            w(r, k, v)
        return r

    def full(conf="probable", verdict="pass", reviewer="adversarial-reviewer", knowledge="none", status="resolved") -> Path:
        files = {"questions/Q-1/log.md": LOG, "questions/Q-1/analysis.md": AN, "questions/Q-1/proof.md": PROOF.format(c=conf),
                 "questions/Q-1/pipeline.md": f"---\nquestion: Q-1\nstatus: open\nknowledge: {knowledge}\n---\n# P\n",
                 "questions/Q-1/plan.md": PLAN.replace("status: open", f"status: {status}")}
        if conf == "proven":
            files["questions/Q-1/review.md"] = REVIEW.format(v=verdict, r=reviewer)
        return repo(files)

    def failing(gates: list[Gate]) -> set[str]:
        return {x.name for x in gates if not x.ok}

    print("pipeline_check.py self-test")
    r = repo()
    ok("plan-only repo passes stages 0 and 1", not failing(evaluate(r, "Q-1", 1)))
    ok("plan-only repo fails the search gate", "search log" in failing(evaluate(r, "Q-1", 2)))
    ok("full good repo passes every gate", not failing(evaluate(full(), "Q-1", 9)))
    ok("a missing question folder fails the repo gate", "research repo" in failing(evaluate(r, "Q-9", 9)))

    sk = Path(tempfile.mkdtemp(prefix="gps-skills-"))
    for rel in (".claude-plugin/plugin.json", "CONVENTIONS.md", "skills/x/SKILL.md", "people/.k", "sources/.k", "questions/Q-1/plan.md"):
        w(sk, rel, "x")
    ok("the skills repo is refused", "research repo" in failing(evaluate(sk, "Q-1", 0)))

    r = repo({"questions/Q-1/log.md": LOG.replace("- **Result:** found\n", "")})
    ok("a log entry without a Result field fails", "search log" in failing(evaluate(r, "Q-1", 2)))
    r = repo({"questions/Q-1/log.md": LOG, "questions/Q-1/muse/M-1.request.md": "---\nrequest: M-1\nquestion: Q-1\nstatus: waiting\n---\n"})
    ok("a Muse request still waiting blocks ingest", "muse requests ingested" in failing(evaluate(r, "Q-1", 3)))
    r = repo({"questions/Q-1/log.md": LOG, "questions/Q-1/muse/M-1.request.md": "---\nrequest: M-1\nquestion: Q-1\nstatus: ingested\n---\n"})
    ok("an ingested request without a result path fails", "muse requests ingested" in failing(evaluate(r, "Q-1", 3)))
    r = repo({"questions/Q-1/log.md": LOG, "questions/Q-1/muse/M-1.request.md": "---\nrequest: M-1\nquestion: Q-1\nstatus: ingested\nresult: inbox/Q-1/M-1/M-1.result.md\n---\n"})
    ok("an ingested request with a result path passes", "muse requests ingested" not in failing(evaluate(r, "Q-1", 3)))
    r = repo({"questions/Q-1/log.md": LOG, "questions/Q-1/analysis.md": AN.replace("## Conflicts", "## Other")})
    ok("analysis without a Conflicts section fails", "analysis" in failing(evaluate(r, "Q-1", 4)))
    r = repo({"questions/Q-1/log.md": LOG, "questions/Q-1/analysis.md": AN})
    ok("missing proof fails", "proof" in failing(evaluate(r, "Q-1", 5)))
    ok("proven without a review fails", "review" in failing(evaluate(repo({"questions/Q-1/log.md": LOG, "questions/Q-1/analysis.md": AN, "questions/Q-1/proof.md": PROOF.format(c="proven")}), "Q-1", 6)))
    ok("proven with a failing review fails", "review" in failing(evaluate(full("proven", "fail"), "Q-1", 6)))
    ok("proven reviewed by the analyst fails (not independent)", "review" in failing(evaluate(full("proven", "pass", "evidence-analyst"), "Q-1", 6)))
    ok("proven reviewed with a blank reviewer fails", "review" in failing(evaluate(full("proven", "pass", ""), "Q-1", 6)))
    ok("proven with an independent passing review passes", "review" not in failing(evaluate(full("proven"), "Q-1", 6)))
    ok("probable needs no review", "review" not in failing(evaluate(full("probable"), "Q-1", 6)))
    ok("stalled question needs the settling record named", "proof" in failing(evaluate(repo({"questions/Q-1/log.md": LOG, "questions/Q-1/analysis.md": AN, "questions/Q-1/plan.md": PLAN.replace("status: open", "status: stalled")}), "Q-1", 5)))
    ok("stalled question that names it passes", "proof" not in failing(evaluate(repo({"questions/Q-1/log.md": LOG, "questions/Q-1/analysis.md": AN.replace("none", "A 1790 tax list would settle it"), "questions/Q-1/plan.md": PLAN.replace("status: open", "status: stalled")}), "Q-1", 5)))
    bad = full()
    w(bad, "people/P-john-cook-1792.md", V.GOOD_PERSON.replace("[[S-1850-census-x]]", ""))
    ok("a validator error fails the validate gate", "validator" in failing(evaluate(bad, "Q-1", 7)))
    ok("missing knowledge line fails", "knowledge capture" in failing(evaluate(full(knowledge=""), "Q-1", 8)))
    ok("an open question fails the close gate", "close" in failing(evaluate(full(status="open"), "Q-1", 9)))

    r = full()
    gates = evaluate(r, "Q-1", 9)
    pl = record(r, "Q-1", gates)
    t1 = pl.read_text(encoding="utf-8")
    record(r, "Q-1", gates)
    t2 = pl.read_text(encoding="utf-8")
    ok("--record writes a gate log", "<!-- gates:start -->" in t1 and "| 9 close |" in t1)
    ok("--record is idempotent and keeps the knowledge line", t2.count("<!-- gates:start -->") == 1 and "knowledge: none" in t2)
    ok("the recorded pipeline.md passes the validator", not V.validate(r).errors)

    # second opinion gate
    def with_so(so_text: str | None, raw: dict | None = None, flag: bool = True) -> Path:
        rr = full("proven")
        if flag:
            w(rr, "questions/Q-1/plan.md", PLAN.replace("status: open", "status: resolved\nsecond_opinion: true"))
        if so_text is not None:
            w(rr, "questions/Q-1/second-opinion.md", so_text)
        if raw is not None:
            w(rr, "inbox/Q-1/agy/review-1.json", json.dumps(raw))
        return rr

    SO = "---\nquestion: Q-1\nstatus: resolved\nkind: review\nmodel: gemini-4-hydrogen-high\nverdict: {v}\nraw: inbox/Q-1/agy/review-1.json\n---\n# So\n"
    GOODRAW = {"status": "SUCCESS", "structured_output": {"verdict": "pass", "findings": []}}
    ok("second opinion not required when the plan does not ask", "second opinion" not in failing(evaluate(full("proven"), "Q-1", 6)))
    ok("second_opinion: true with no file fails", "second opinion" in failing(evaluate(with_so(None), "Q-1", 6)))
    ok("a failing second opinion fails", "second opinion" in failing(evaluate(with_so(SO.format(v="fail"), GOODRAW), "Q-1", 6)))
    ok("a passing second opinion with a matching raw reply passes", "second opinion" not in failing(evaluate(with_so(SO.format(v="pass"), GOODRAW), "Q-1", 6)))
    ok("a pass with an unsuccessful raw reply fails", "second opinion" in failing(evaluate(with_so(SO.format(v="pass"), {"status": "ERROR"}), "Q-1", 6)))
    ok("a pass with no model recorded fails", "second opinion" in failing(evaluate(with_so(SO.format(v="pass").replace("model: gemini-4-hydrogen-high", "model:"), GOODRAW), "Q-1", 6)))
    ok("a pass whose raw reply is elsewhere is a warning, not a failure", "second opinion" not in failing(evaluate(with_so(SO.format(v="pass")), "Q-1", 6)))
    ok("probable claims do not need a second opinion", "second opinion" not in failing(evaluate(with_so(None, flag=True) if False else full("probable"), "Q-1", 6)))

    print("PASS" if not failures else f"FAILED: {failures}")
    return 0 if not failures else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("--")]
    through = 9
    if "--through" in argv:
        through = int(argv[argv.index("--through") + 1])
        args = [a for a in args if a != str(through)]
    if len(args) != 2:
        print(__doc__)
        return 2
    repo, q = Path(args[0]).resolve(), args[1]
    gates = evaluate(repo, q, through)
    print(render(gates))
    if "--record" in argv and (repo / "questions" / q).is_dir():
        print("recorded in", record(repo, q, gates))
    failed = [x for x in gates if not x.ok]
    print(f"\n{len(failed)} gate(s) failed through stage {through}." if failed else f"\nAll gates through stage {through} passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
