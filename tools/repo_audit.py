#!/usr/bin/env python3
"""Audit a repository against public-facing, industry-standard repository hygiene.

Usage:
    python3 repo_audit.py [REPO] [--github [OWNER/REPO]] [--allow-root name,name] [--json]
    python3 repo_audit.py --self-test

Checks (ERROR blocks, WARN should be fixed, INFO is advice):
  community files, README quality, internal links, placeholders, directory indexes, root clutter, file naming and junk,
  large files, secrets, changelog, citation file, commit-message convention, and (for research repos) the data validator.
  --github adds repository settings: description, topics, license, branch protection, community profile, and visibility.
Exit code 0 = no errors. Standard library only. No network access except `gh`, and only with --github.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_here = Path(__file__).resolve().parent
for _cand in (_here, _here.parent.parent / "repo-schema-validate" / "scripts"):
    if (_cand / "validate.py").is_file():
        sys.path.insert(0, str(_cand))
        break
try:
    import validate as V  # noqa: E402
except ImportError:  # the audit also works on repos that are not research repos
    V = None

LARGE_WARN, LARGE_ERR = 5_000_000, 50_000_000
ROOT_ALLOW = {
    "README.md", "LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md",
    "SUPPORT.md", "CITATION.cff", "CHANGELOG.md", "CODEOWNERS", "INDEX.md", "CONVENTIONS.md", "METHODS.md", "ETHICS.md",
    "CLAUDE.md", "AGENTS.md", ".gitignore", ".gitattributes", ".editorconfig", "install.sh", "pyproject.toml", "Makefile",
    "package.json", "codemeta.json", ".zenodo.json", ".nojekyll",
}
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
JUNK_RE = re.compile(r"(?i)(\.bak|\.tmp|\.swp|\.orig|\.pyc|~)$")
MESSY_RE = re.compile(r"(?i)(?:^|[ _.-])(final|copy|backup|old|draft|untitled)(?:[ _.-]|$)|\(\d+\)")
SECRET_RES = [
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"), "a private key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "an AWS access key"),
    (re.compile(r"\bghp_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "a GitHub token"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "a Slack token"),
    (re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"]?[A-Za-z0-9/+_-]{16,}"), "a hard-coded credential"),
]
CONVENTIONAL = re.compile(r"^(?:feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|data|research|knowledge)(?:\([\w./-]+\))?!?: .+|^Merge |^Revert ")
DOC_ROOTS = ["README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md", "CHANGELOG.md", "METHODS.md", "ETHICS.md", "CITATION.cff"]
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|!\[[^\]]*\]\(([^)\s]+)\)")


class F:
    def __init__(self, sev: str, code: str, msg: str, path: str = "") -> None:
        self.sev, self.code, self.msg, self.path = sev, code, msg, path

    def line(self) -> str:
        return f"{self.sev:5} {self.code:<18} {self.path + ': ' if self.path else ''}{self.msg}"


def tracked(repo: Path) -> list[str]:
    try:
        out = subprocess.run(["git", "-C", str(repo), "ls-files", "--cached", "--others", "--exclude-standard"], capture_output=True, text=True, check=True).stdout.split("\n")
        files = [f for f in out if f]
        if files:
            return [f for f in files if (repo / f).exists()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    skip = {".git", "inbox", "node_modules", "__pycache__"}
    res = []
    for p in repo.rglob("*"):
        rel = p.relative_to(repo)
        if p.is_file() and not (set(rel.parts) & skip):
            res.append(str(rel))
    return sorted(res)


def find_any(files: set[str], names: list[str], dirs=("", ".github/", "docs/")) -> str | None:
    for d in dirs:
        for n in names:
            if d + n in files:
                return d + n
    return None


def is_template_path(rel: str) -> bool:
    parts = rel.split("/")
    return "templates" in parts or "examples" in parts or rel.endswith(".tmpl") or ".github/ISSUE_TEMPLATE" in rel


def audit(repo: Path, allow_root: set[str] | None = None) -> list[F]:
    out: list[F] = []
    files = tracked(repo)
    fset = set(files)
    allow = ROOT_ALLOW | (allow_root or set())

    # ---- community files
    for label, names, sev in (
        ("README", ["README.md"], "ERROR"), ("LICENSE", ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"], "ERROR"),
        ("CONTRIBUTING", ["CONTRIBUTING.md"], "ERROR"), ("CODE_OF_CONDUCT", ["CODE_OF_CONDUCT.md"], "ERROR"),
        ("SECURITY", ["SECURITY.md"], "ERROR"), ("CITATION", ["CITATION.cff"], "ERROR"), ("CHANGELOG", ["CHANGELOG.md"], "ERROR"),
        ("SUPPORT", ["SUPPORT.md"], "WARN"), ("CODEOWNERS", ["CODEOWNERS"], "WARN"),
    ):
        if not find_any(fset, names, dirs=("",) if label in {"README", "LICENSE", "CITATION", "CHANGELOG"} else ("", ".github/", "docs/")):
            out.append(F(sev, "community-file", f"missing {label} ({' or '.join(names)})"))
    if not any(f.startswith(".github/ISSUE_TEMPLATE/") for f in files):
        out.append(F("ERROR", "issue-template", "no issue template under .github/ISSUE_TEMPLATE/"))
    elif ".github/ISSUE_TEMPLATE/config.yml" not in fset:
        out.append(F("WARN", "issue-template", "no .github/ISSUE_TEMPLATE/config.yml (set blank_issues_enabled and contact links)"))
    if not find_any(fset, ["pull_request_template.md", "PULL_REQUEST_TEMPLATE.md"], dirs=(".github/", "docs/", "")):
        out.append(F("ERROR", "pr-template", "no pull request template (.github/pull_request_template.md)"))
    if not any(f.startswith(".github/workflows/") for f in files):
        out.append(F("WARN", "ci", "no GitHub Actions workflow (validation should run on every pull request)"))

    # ---- README quality
    if "README.md" in fset:
        t = (repo / "README.md").read_text(encoding="utf-8", errors="replace")
        lines = t.splitlines()
        if not re.search(r"^#\s+\S", t, re.M):
            out.append(F("ERROR", "readme", "no H1 title", "README.md"))
        paras = [p.strip() for p in re.split(r"\n\s*\n", re.sub(r"^#.*$", "", t, flags=re.M)) if p.strip() and not p.strip().startswith(("[!", "![", "<", "|", "```"))]
        if not paras or len(paras[0]) < 40:
            out.append(F("ERROR", "readme", "no description paragraph of at least 40 characters under the title", "README.md"))
        for want, rx in (("citation", r"^#{1,3}\s*(?:how to )?cite|^#{1,3}\s*citation"), ("license", r"^#{1,3}\s*licen[cs]e"),
                         ("contributing", r"^#{1,3}\s*contribut")):
            if not re.search(rx, t, re.M | re.I):
                out.append(F("WARN", "readme", f"no '{want}' section", "README.md"))
        if len(lines) > 120 and not re.search(r"(?i)table of contents|^#{1,3}\s*contents", t, re.M):
            out.append(F("WARN", "readme", "longer than 120 lines with no table of contents", "README.md"))

    # ---- placeholders
    for rel in files:
        if is_template_path(rel) or not (rel in DOC_ROOTS or rel.startswith("docs/")):
            continue
        t = (repo / rel).read_text(encoding="utf-8", errors="replace")
        if "{{" in t:
            out.append(F("ERROR", "placeholder", "unresolved {{placeholder}}", rel))
        if re.search(r"\b(?:TODO|FIXME|TBD)\b|lorem ipsum", t, re.I):
            out.append(F("WARN", "placeholder", "contains TODO, FIXME, TBD, or filler text", rel))

    # ---- internal links
    for rel in files:
        if not rel.endswith(".md") or rel.startswith("inbox/") or is_template_path(rel):
            continue
        t = (repo / rel).read_text(encoding="utf-8", errors="replace")
        t = re.sub(r"```.*?```", "", t, flags=re.S)
        for m in LINK_RE.finditer(t):
            target = (m.group(1) or m.group(2) or "").strip()
            if not target or re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|\{\{)", target, re.I):
                continue
            path = target.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            dest = (repo / path.lstrip("/")) if path.startswith("/") else (repo / Path(rel).parent / path)
            try:
                dest.resolve().relative_to(repo.resolve())
            except ValueError:
                out.append(F("ERROR", "broken-link", f"link leaves the repository: {target}", rel))
                continue
            if not dest.exists():
                out.append(F("ERROR", "broken-link", f"link target does not exist: {target}", rel))

    # ---- structure
    for d in sorted({f.split("/")[0] for f in files if "/" in f}):
        if d.startswith(".") or d in {"inbox", "exports"}:
            continue
        if not any(f in fset for f in (f"{d}/README.md", f"{d}/index.md", f"{d}/INDEX.md")):
            out.append(F("WARN", "dir-index", f"top-level folder '{d}/' has no README.md explaining what it holds"))
    for f in files:
        if "/" not in f and f not in allow and not f.startswith("."):
            out.append(F("WARN", "root-clutter", f"'{f}' is not a standard root file; move it into a folder (or allow it with --allow-root)"))
    if (repo / "docs").is_dir() and not any(f in fset for f in ("docs/README.md", "docs/index.md")):
        out.append(F("WARN", "docs-index", "docs/ has no README.md or index.md"))

    # ---- names, junk, size
    lfs = ""
    if ".gitattributes" in fset:
        lfs = (repo / ".gitattributes").read_text(encoding="utf-8", errors="replace")
    for f in files:
        base = f.split("/")[-1]
        if base in JUNK_NAMES or JUNK_RE.search(base) or "__pycache__" in f:
            out.append(F("ERROR", "junk-file", "editor, OS, or build junk is tracked; remove it and add it to .gitignore", f))
        elif " " in f or MESSY_RE.search(base):
            out.append(F("WARN", "file-name", "name has a space or looks like a leftover (final, copy, old, draft, (1)); use clear kebab-case names", f))
        size = (repo / f).stat().st_size
        ext_lfs = bool(lfs) and "filter=lfs" in lfs and re.search(rf"\*\.{re.escape(Path(f).suffix.lstrip('.'))}\b.*filter=lfs", lfs) is not None
        if size > LARGE_ERR:
            out.append(F("ERROR", "large-file", f"{size // 1_000_000} MB; GitHub rejects files over 100 MB and repositories bloat; use Git LFS or release assets", f))
        elif size > LARGE_WARN and not ext_lfs:
            out.append(F("WARN", "large-file", f"{size // 1_000_000} MB and not under Git LFS", f))

    # ---- secrets
    for f in files:
        p = repo / f
        if p.stat().st_size > 1_000_000 or p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".webp"}:
            continue
        if f.endswith(".py") and ("/scripts/" in f or f.startswith("tools/")):
            continue  # scripts hold example secret patterns in their pattern tables and tests
        t = p.read_text(encoding="utf-8", errors="replace")
        for rx, what in SECRET_RES:
            if rx.search(t):
                out.append(F("ERROR", "secret", f"looks like {what}; remove it, rewrite history if it was pushed, and rotate the secret", f))
                break

    # ---- changelog and citation
    if "CHANGELOG.md" in fset:
        t = (repo / "CHANGELOG.md").read_text(encoding="utf-8", errors="replace")
        if not re.search(r"^##\s*\[?(?:Unreleased|v?\d[\w.-]*)\]?", t, re.M | re.I):
            out.append(F("WARN", "changelog", "no '## [Unreleased]' or version heading (Keep a Changelog format)", "CHANGELOG.md"))
    if "CITATION.cff" in fset:
        t = (repo / "CITATION.cff").read_text(encoding="utf-8", errors="replace")
        for k in ("cff-version", "message", "title", "authors"):
            if not re.search(rf"^{k}\s*:", t, re.M):
                out.append(F("ERROR", "citation", f"missing key '{k}'", "CITATION.cff"))
        for k in ("version", "date-released", "license"):
            if not re.search(rf"^{k}\s*:", t, re.M):
                out.append(F("WARN", "citation", f"missing key '{k}'", "CITATION.cff"))
    lic = find_any(fset, ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"], dirs=("",))
    if lic and (repo / lic).stat().st_size < 200:
        out.append(F("ERROR", "license", "license file looks empty or truncated; use the official text", lic))

    # ---- commit messages
    try:
        subjects = subprocess.run(["git", "-C", str(repo), "log", "-30", "--pretty=%s"], capture_output=True, text=True, check=True).stdout.splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError):
        subjects = []
    bad = [s for s in subjects if not CONVENTIONAL.match(s)]
    if subjects and len(bad) / len(subjects) > 0.2:
        out.append(F("WARN", "commit-style", f"{len(bad)} of the last {len(subjects)} commit subjects do not follow Conventional Commits (type(scope): subject), e.g. {bad[0][:60]!r}"))

    # ---- research data
    if V is not None and all((repo / d).is_dir() for d in ("people", "sources", "questions")):
        rep = V.validate(repo)
        if rep.errors:
            out.append(F("ERROR", "data-validator", f"{len(rep.errors)} research-data validator error(s); first: {rep.errors[0][:110]}"))
        living = [w for w in rep.warnings if "living person" in w]
        if living:
            out.append(F("WARN", "living-people", f"{len(living)} living or recent person file(s); the repository must be private, or they must be removed, before it is public"))
    return out


def github_checks(repo: Path, slug: str | None, has_living: bool) -> list[F]:
    gh = os.environ.get("GH_BIN", "gh")

    def api(path: str) -> dict | None:
        try:
            r = subprocess.run([gh, "api", path], capture_output=True, text=True, timeout=30, cwd=repo)
            return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            return None

    out: list[F] = []
    if not slug:
        try:
            r = subprocess.run([gh, "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"], capture_output=True, text=True, timeout=20, cwd=repo)
            slug = r.stdout.strip() or None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            slug = None
    meta = api(f"repos/{slug}") if slug else None
    if not meta:
        return [F("WARN", "github", "GitHub checks skipped (no gh, no network, or repo not found)")]
    if not (meta.get("description") or "").strip():
        out.append(F("WARN", "gh-description", "repository has no description"))
    if len(meta.get("topics") or []) < 3:
        out.append(F("WARN", "gh-topics", "fewer than 3 topics; add topics so researchers can find the repository"))
    if not meta.get("license"):
        out.append(F("WARN", "gh-license", "GitHub does not detect a license"))
    if meta.get("has_issues") is False:
        out.append(F("WARN", "gh-issues", "issues are disabled; researchers cannot submit corrections"))
    branch = meta.get("default_branch") or "main"
    if api(f"repos/{slug}/branches/{branch}/protection") is None:
        out.append(F("WARN", "gh-protection", f"default branch '{branch}' has no branch protection (require a pull request and the validation check)"))
    prof = api(f"repos/{slug}/community/profile")
    if prof and isinstance(prof.get("health_percentage"), int) and prof["health_percentage"] < 100:
        out.append(F("INFO", "gh-community", f"GitHub community profile is {prof['health_percentage']}%"))
    if meta.get("visibility") == "public" and has_living:
        out.append(F("ERROR", "gh-public-living", "the repository is PUBLIC and holds living or recent person files"))
    return out


# ----------------------------------------------------------------------------- self-test

GOOD = {
    "README.md": "# Cook Lineage Research\n\nA documented study of the Cook families of Pittsylvania County, Virginia, built to the Genealogical Proof Standard.\n\n## How to cite\nSee CITATION.cff.\n\n## Contributing\nSee [CONTRIBUTING.md](CONTRIBUTING.md).\n\n## License\nCC BY 4.0.\n",
    "LICENSE": "License text. " * 30,
    "CONTRIBUTING.md": "# Contributing\nOpen an issue.\n",
    "CODE_OF_CONDUCT.md": "# Code of conduct\nBe kind.\n",
    "SECURITY.md": "# Security\nReport privately.\n",
    "SUPPORT.md": "# Support\nOpen an issue.\n",
    "CODEOWNERS": "* @owner\n",
    "CITATION.cff": "cff-version: 1.2.0\nmessage: cite\ntitle: t\nauthors:\n  - name: a\nversion: 1.0.0\ndate-released: 2026-11-27\nlicense: CC-BY-4.0\n",
    "CHANGELOG.md": "# Changelog\n\n## [Unreleased]\n",
    ".github/pull_request_template.md": "## What\n",
    ".github/ISSUE_TEMPLATE/bug.yml": "name: Bug\n",
    ".github/ISSUE_TEMPLATE/config.yml": "blank_issues_enabled: false\n",
    ".github/workflows/ci.yml": "name: ci\n",
    "docs/README.md": "# Docs\n",
    "tools/README.md": "# Tools\n",
}


def self_test() -> int:
    global LARGE_WARN, LARGE_ERR
    failures: list[str] = []

    def ok(name: str, cond: bool) -> None:
        print(f"  {'ok  ' if cond else 'FAIL'} {name}")
        if not cond:
            failures.append(name)

    def repo(extra: dict | None = None, drop: tuple = (), git: bool = False) -> Path:
        r = Path(tempfile.mkdtemp(prefix="gps-audit-"))
        for k, v in {**GOOD, **(extra or {})}.items():
            if k in drop:
                continue
            p = r / k
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(v, encoding="utf-8")
        if git:
            subprocess.run(["git", "-C", str(r), "init", "-q"], check=True)
        return r

    def codes(r: Path, sev: str | None = None, **kw) -> set[str]:
        return {f.code for f in audit(r, **kw) if sev is None or f.sev == sev}

    print("repo_audit.py self-test")
    ok("a compliant repository has no errors or warnings", not audit(repo()))
    for name in ("LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "CITATION.cff", "CHANGELOG.md", "README.md"):
        ok(f"missing {name} is an error", "community-file" in codes(repo(drop=(name,)), "ERROR") or name == "README.md" and "community-file" in codes(repo(drop=(name,)), "ERROR"))
    ok("missing SUPPORT.md is only a warning", "community-file" in codes(repo(drop=("SUPPORT.md",)), "WARN") and "community-file" not in codes(repo(drop=("SUPPORT.md",)), "ERROR"))
    ok("a missing PR template is an error", "pr-template" in codes(repo(drop=(".github/pull_request_template.md",)), "ERROR"))
    ok("missing issue templates are an error", "issue-template" in codes(repo(drop=(".github/ISSUE_TEMPLATE/bug.yml", ".github/ISSUE_TEMPLATE/config.yml")), "ERROR"))
    ok("a README without a description is an error", "readme" in codes(repo({"README.md": "# T\n\nhi\n\n## License\n## Contributing\n## Cite\n"}), "ERROR"))
    ok("a README without a license section warns", "readme" in codes(repo({"README.md": GOOD["README.md"].replace("## License\nCC BY 4.0.\n", "")}), "WARN"))
    ok("a broken internal link is an error", "broken-link" in codes(repo({"README.md": GOOD["README.md"] + "\nSee [guide](docs/missing.md).\n"}), "ERROR"))
    ok("a link that leaves the repository is an error", "broken-link" in codes(repo({"README.md": GOOD["README.md"] + "\n[x](../../etc/passwd)\n"}), "ERROR"))
    ok("links with anchors and external URLs are fine", not codes(repo({"README.md": GOOD["README.md"] + "\n[a](CONTRIBUTING.md#top) [b](https://example.org/x) [c](#cite)\n"}), "ERROR"))
    ok("links inside code fences are ignored", not codes(repo({"README.md": GOOD["README.md"] + "\n```\n[x](nope.md)\n```\n"}), "ERROR"))
    ok("an unresolved {{placeholder}} is an error", "placeholder" in codes(repo({"README.md": GOOD["README.md"] + "\n{{AUTHOR}}\n"}), "ERROR"))
    ok("placeholders inside templates/ are ignored", not codes(repo({"docs/templates/x.md": "{{A}}"}), "ERROR"))
    ok("TODO text warns", "placeholder" in codes(repo({"CONTRIBUTING.md": "# C\nTODO write this\n"}), "WARN"))
    ok("a folder without a README warns", "dir-index" in codes(repo({"misc/data.csv": "a,b\n"}), "WARN"))
    ok("root clutter warns", "root-clutter" in codes(repo({"notes final.txt": "x"}), "WARN"))
    ok("--allow-root permits a named file", "root-clutter" not in codes(repo({"extra.txt": "x"}), "WARN", allow_root={"extra.txt"}))
    ok("a messy file name warns", "file-name" in codes(repo({"docs/report final copy.md": "# r\n"}), "WARN"))
    ok("tracked junk is an error", "junk-file" in codes(repo({".DS_Store": "x"}), "ERROR"))
    LARGE_WARN, LARGE_ERR = 1000, 5000
    ok("a large file warns", "large-file" in codes(repo({"docs/big.txt": "x" * 2000}), "WARN"))
    ok("a very large file is an error", "large-file" in codes(repo({"docs/huge.txt": "x" * 6000}), "ERROR"))
    ok("a large file under LFS does not warn", "large-file" not in codes(repo({"docs/big.pdf": "x" * 2000, ".gitattributes": "*.pdf filter=lfs diff=lfs merge=lfs -text\n"}), "WARN"))
    LARGE_WARN, LARGE_ERR = 5_000_000, 50_000_000
    ok("a private key is an error", "secret" in codes(repo({"docs/k.txt": "-----BEGIN RSA PRIVATE KEY-----\nabc\n"}), "ERROR"))
    ok("a GitHub token is an error", "secret" in codes(repo({"docs/t.txt": "ghp_" + "a" * 36}), "ERROR"))
    ok("a hard-coded credential is an error", "secret" in codes(repo({"docs/c.txt": "api_key = abcdef0123456789abcdef"}), "ERROR"))
    ok("a changelog without headings warns", "changelog" in codes(repo({"CHANGELOG.md": "# Changelog\nstuff\n"}), "WARN"))
    ok("a citation file without a title is an error", "citation" in codes(repo({"CITATION.cff": "cff-version: 1.2.0\nmessage: m\nauthors:\n  - name: a\n"}), "ERROR"))
    ok("a truncated license is an error", "license" in codes(repo({"LICENSE": "MIT"}), "ERROR"))

    r = repo(git=True)
    for msg in ("feat: add x", "fix(data): y", "docs: z"):
        subprocess.run(["git", "-C", str(r), "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", msg], check=True)
    ok("conventional commits pass", "commit-style" not in codes(r))
    for msg in ("stuff", "more stuff", "wip"):
        subprocess.run(["git", "-C", str(r), "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", msg], check=True)
    ok("non-conventional commits warn", "commit-style" in codes(r, "WARN"))

    if V is not None:
        data = {"people/README.md": "# People\n", "sources/README.md": "# Sources\n", "questions/README.md": "# Questions\n",
                "sources/S-1850-census-x.md": V.GOOD_SOURCE, "people/P-john-cook-1792.md": V.GOOD_PERSON.replace("questions: [Q-1]\n", ""),
                }
        ok("a valid research repo passes the data check", "data-validator" not in codes(repo(data)))
        bad = dict(data, **{"people/P-john-cook-1792.md": V.GOOD_PERSON.replace("[[S-1850-census-x]]", "").replace("questions: [Q-1]\n", "")})
        ok("a research-data error is an audit error", "data-validator" in codes(repo(bad), "ERROR"))
        live = dict(data, **{"people/P-john-cook-1792.md": V.GOOD_PERSON.replace("living: false", "living: true").replace("questions: [Q-1]\n", "")})
        ok("living people warn", "living-people" in codes(repo(live), "WARN"))

    tmp = Path(tempfile.mkdtemp())
    fake = tmp / "fake_gh.py"
    fake.write_text('''#!/usr/bin/env python3
import json, os, sys
a = sys.argv[1:]
mode = os.environ.get("FAKE_GH", "good")
if a[:2] == ["repo", "view"]: print("o/r"); sys.exit(0)
path = a[1] if len(a) > 1 else ""
if mode == "down": sys.exit(1)
if path.endswith("/protection"):
    if mode == "unprotected": sys.exit(1)
    print(json.dumps({"url": "x"})); sys.exit(0)
if path.endswith("/community/profile"): print(json.dumps({"health_percentage": 80})); sys.exit(0)
meta = {"description": "d", "topics": ["a", "b", "c"], "license": {"key": "cc-by-4.0"}, "has_issues": True, "default_branch": "main", "visibility": "private"}
if mode == "bare": meta.update(description="", topics=[], license=None)
if mode == "public": meta["visibility"] = "public"
print(json.dumps(meta))
''', encoding="utf-8")
    fake.chmod(0o755)
    os.environ["GH_BIN"] = str(fake)
    r0 = repo()
    for mode, expect, label in (("good", set(), "a well-configured GitHub repo has no findings beyond info"),
                                ("bare", {"gh-description", "gh-topics", "gh-license"}, "a bare GitHub repo warns on description, topics, and license"),
                                ("unprotected", {"gh-protection"}, "an unprotected default branch warns"), ("down", {"github"}, "an unreachable GitHub is a skipped-check warning, not a failure")):
        os.environ["FAKE_GH"] = mode
        got = {f.code for f in github_checks(r0, None, False) if f.sev != "INFO"}
        ok(label, got == expect)
    os.environ["FAKE_GH"] = "public"
    ok("a public repo with living people is an error", "gh-public-living" in {f.code for f in github_checks(r0, "o/r", True) if f.sev == "ERROR"})
    ok("a public repo without living people is fine", not [f for f in github_checks(r0, "o/r", False) if f.sev == "ERROR"])

    print("PASS" if not failures else f"FAILED: {failures}")
    return 0 if not failures else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("--")]
    allow: set[str] = set()
    slug = None
    if "--allow-root" in argv:
        v = argv[argv.index("--allow-root") + 1]
        allow = {x for x in v.split(",") if x}
        args = [a for a in args if a != v]
    use_gh = "--github" in argv
    if use_gh:
        i = argv.index("--github")
        if i + 1 < len(argv) and re.fullmatch(r"[\w.-]+/[\w.-]+", argv[i + 1]):
            slug = argv[i + 1]
            args = [a for a in args if a != slug]
    repo = Path(args[0] if args else ".").resolve()
    findings = audit(repo, allow)
    if use_gh:
        findings += github_checks(repo, slug, any(f.code == "living-people" for f in findings))
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: (order[f.sev], f.code, f.path))
    if "--json" in argv:
        print(json.dumps([f.__dict__ for f in findings], indent=2))
    else:
        for f in findings:
            print(f.line())
    n = {s: sum(1 for f in findings if f.sev == s) for s in order}
    print(f"\n{n['ERROR']} error(s), {n['WARN']} warning(s), {n['INFO']} info.", "Ready for the public." if not n["ERROR"] else "Not ready for the public.")
    return 1 if n["ERROR"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
