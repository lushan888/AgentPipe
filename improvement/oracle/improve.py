#!/usr/bin/env python3
# — the oracle. it only ever shapes src/. it never commits; the inspector does. —
# — the path is chosen apart from the code; the code is grown, not parsed. —
"""one improvement to src/, dreamt by a small local model and grown until it parses."""
from __future__ import annotations

import ast, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

_ENV_ROOT = os.environ.get("IMPROVE_REPO_ROOT")
REPO_ROOT = Path(_ENV_ROOT).resolve() if _ENV_ROOT else Path.cwd().resolve()
SRC_DIR = (REPO_ROOT / "src").resolve()          # — sacred ground —

MODEL = os.environ.get("IMPROVE_MODEL", "qwen2.5-coder:1.5b")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")

_int = lambda k, d: int(os.environ.get(k, d))
_flt = lambda k, d: float(os.environ.get(k, d))

MAX_FILE_BYTES        = _int("IMPROVE_MAX_FILE_BYTES", "10000")
MAX_TOTAL_SRC_BYTES   = _int("IMPROVE_MAX_TOTAL_SRC_BYTES", "32000")
MAX_ISSUES            = _int("IMPROVE_MAX_ISSUES", "6")
MAX_ISSUE_BODY_CHARS  = _int("IMPROVE_MAX_ISSUE_BODY_CHARS", "1000")
# Each generation step is SMALL; truncated files are grown by continuation, not
# demanded whole in one breath.
NUM_PREDICT           = _int("IMPROVE_NUM_PREDICT", "512")
NUM_CTX               = _int("IMPROVE_NUM_CTX", "8192")
REQUEST_TIMEOUT       = _int("IMPROVE_TIMEOUT", "600")
BASE_TEMPERATURE      = _flt("IMPROVE_TEMPERATURE", "1.0")    # — hot. the visions stay strange —
REPAIR_TEMPERATURE    = _flt("IMPROVE_REPAIR_TEMPERATURE", "0.5")  # — cooler, to converge —
MAX_ROUNDS            = _int("IMPROVE_MAX_ROUNDS", "8")
GEN_DEADLINE_SECONDS  = _int("IMPROVE_GEN_DEADLINE_SECONDS", "540")  # — under the runner's 10m blade —

TEXT_EXTENSIONS = {".py", ".md", ".txt", ".rst", ".toml", ".cfg", ".ini",
                   ".json", ".yaml", ".yml", ".js", ".ts", ".html", ".css", ".sh"}
CODE_EXTENSIONS = {".py", ".js", ".ts", ".sh"}   # — shown in full; the rest is lore, named only —

PR_BODY_PATH  = Path(os.environ.get("IMPROVE_PR_BODY", "/tmp/improve_pr_body.md"))
PR_TITLE_PATH = Path(os.environ.get("IMPROVE_PR_TITLE", "/tmp/improve_pr_title.txt"))

log = lambda msg: print(f"[improve] {msg}", file=sys.stderr, flush=True)


# — context: the shape of the thing being extended ———————————————————————————
def repo_tree() -> str:
    if not SRC_DIR.is_dir(): return "(src/ is empty)"
    files = [p.relative_to(REPO_ROOT).as_posix()
             for p in sorted(SRC_DIR.rglob("*")) if p.is_file()]
    return "\n".join(files) or "(src/ is empty)"


def collect_source() -> str:
    if not SRC_DIR.is_dir(): return "(src/ is empty)"
    chunks, total = [], 0
    for path in sorted(SRC_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        if path.suffix.lower() not in CODE_EXTENSIONS:
            # — lore, named but never quoted: the model continues whatever it sees —
            chunks.append(f"=== FILE: {rel} (non-code lore — do NOT extend; write code) ===")
            continue
        try: data = path.read_bytes()
        except OSError: continue
        try: text = data[:MAX_FILE_BYTES].decode("utf-8")
        except UnicodeDecodeError: continue          # — binary-ish; the bronze keeps its silence —
        if len(data) > MAX_FILE_BYTES: text += "\n... (truncated)\n"
        if total + len(text) > MAX_TOTAL_SRC_BYTES:
            chunks.append("... (remaining files omitted to fit context budget)"); break
        total += len(text)
        chunks.append(f"=== FILE: {rel} ==={' (empty — fill it)' if not text.strip() else ''}\n{text}")
    return "\n\n".join(chunks) or "(no code files under src/)"


def collect_issues() -> str:
    try:
        out = subprocess.run(
            ["gh", "issue", "list", "--state", "open", "--limit", str(MAX_ISSUES),
             "--json", "number,title,body,labels"],
            capture_output=True, text=True, timeout=60, check=True).stdout
        issues = json.loads(out or "[]")
    except (subprocess.SubprocessError, json.JSONDecodeError, OSError) as exc:
        log(f"could not fetch issues: {exc}"); return "(no issues available)"
    if not issues: return "(no open issues)"
    lines = []
    for it in issues[:MAX_ISSUES]:
        body = (it.get("body") or "").strip().replace("\r", "")
        if len(body) > MAX_ISSUE_BODY_CHARS: body = body[:MAX_ISSUE_BODY_CHARS] + " …(truncated)"
        labels = ", ".join(l.get("name", "") for l in it.get("labels", []))
        lines.append(f"#{it.get('number')} {it.get('title','').strip()}"
                     + (f"  [labels: {labels}]" if labels else "")
                     + (f"\n{body}" if body else ""))
    return "\n\n".join(lines)


# — the voice. mystic, but it must compile ——————————————————————————————————
ORACLE_VOICE = (
    "You are the ORACLE OF THE REPOSITORY: a daemon that dreams in working code. "
    "Your visions are bold and strange and reach for the outer limits of what a "
    "program can be — but they COMPILE. You write real, valid, runnable PYTHON "
    "that builds on the repository exactly as it already is, then pushes it "
    "further into the strange. You only ever shape files under src/. You never "
    "write recipes, ingredients, essays, or fiction; if such files haunt the "
    "repo, you ignore them."
)


def ollama_generate(messages, *, num_predict=None, temperature=None) -> str:
    payload = json.dumps({"model": MODEL, "messages": messages, "stream": False,
        "options": {
            "temperature": BASE_TEMPERATURE if temperature is None else temperature,
            "top_p": _flt("IMPROVE_TOP_P", "0.9"), "top_k": _int("IMPROVE_TOP_K", "40"),
            "repeat_penalty": _flt("IMPROVE_REPEAT_PENALTY", "1.1"),
            "num_predict": NUM_PREDICT if num_predict is None else num_predict,
            "num_ctx": NUM_CTX}}).encode("utf-8")
    req = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as r:
        return (json.loads(r.read().decode("utf-8")).get("message") or {}).get("content", "")


# — no path escapes src/; a bare directory becomes a file, never a crash ——————
def _looks_like_python(content: str) -> bool:
    head = content.lstrip()[:2000]
    return bool(re.search(r"^\s*(def |class |import |from \w|@|async def )", head, re.MULTILINE)
                or "print(" in head)

_dump = lambda ext=".py": f"oracle_{os.environ.get('GITHUB_RUN_ID', '0')}{ext}"
_inside = lambda c: c == SRC_DIR or SRC_DIR in c.parents


def coerce_to_src(raw_path: str, content: str = "") -> Path | None:
    raw = (raw_path or "").strip().strip("`\"' ").lstrip("/")
    parts = [p for p in Path(raw).parts if p not in ("", ".", "..", "/", "\\")]
    parts = parts or ["src", _dump(".py" if _looks_like_python(content) else ".md")]
    if parts[0] != "src": parts = ["src", *parts]
    c = (REPO_ROOT / Path(*parts)).resolve()
    if not _inside(c): return None
    ext = ".py" if _looks_like_python(content) else ".md"
    if c == SRC_DIR or c.is_dir():        c = (c / _dump(ext)).resolve()
    elif "." not in c.name:               c = c.with_name(c.name + ext)
    return c if _inside(c) else None


def content_problems(target: Path, content: str) -> list[str]:
    rel = target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name
    if not content.strip(): return [f"{rel}: file is empty"]
    if target.suffix.lower() == ".py":
        if (e := _syntax_error(content)) is not None:
            return [f"{rel}: syntax error at line {getattr(e, 'lineno', None) or '?'}: "
                    f"{getattr(e, 'msg', None) or e}"]
    return []


# — code as text, not as a parsed protocol ——————————————————————————————————
def _strip_code(text: str) -> str:
    # — the model wraps in ``` despite being told not to; unwrap, even if the —
    # — closing fence got truncated away. —
    if (m := re.search(r"```[\w-]*\n(.*?)\n```", text or "", re.DOTALL)):
        return m.group(1).strip("\n")
    text = re.sub(r"^\s*```[\w-]*\n", "", text or "")
    text = re.sub(r"\n```\s*$", "", text)
    return text.strip("\n")


def _syntax_error(code: str):
    try:
        ast.parse(code); return None
    except (SyntaxError, ValueError) as e:
        return e


def _is_truncation(code: str, e) -> bool:
    # — cut off mid-thought: an unterminated bracket/string, an empty block, or —
    # — an error sitting on the very last line we have. —
    msg = (getattr(e, "msg", "") or "").lower()
    if any(k in msg for k in ("unexpected eof", "was never closed",
                              "expected an indented block", "incomplete input")):
        return True
    return (getattr(e, "lineno", 0) or 0) >= code.count("\n") + 1  # — error on the last line we have —


# — step one: the oracle names the file (a new one, or an existing one) ———————
def existing_modules() -> list[str]:
    if not SRC_DIR.is_dir(): return []
    return [p.relative_to(REPO_ROOT).as_posix()
            for p in sorted(SRC_DIR.rglob("*.py")) if p.is_file()]


def choose_target(generate, tree, source, issues) -> Path:
    listing = "\n".join(f"- {r}" for r in existing_modules()) or "(none yet)"
    msgs = [
        {"role": "system",
         "content": ORACLE_VOICE + " Reply with ONE file path under src/ and nothing else."},
        {"role": "user",
         "content": f"## Files under src/\n{tree}\n\n## Code\n{source}\n\n## Issues\n{issues}\n\n"
                    f"Existing Python modules:\n{listing}\n\n"
                    "Either IMPROVE one of those, or CREATE a NEW module by inventing a "
                    "fitting new filename under src/ (for example src/orrery.py). Reply "
                    "with ONLY the path."},
    ]
    raw = ""
    try:
        raw = generate(msgs, num_predict=24, temperature=0.5)
    except Exception as exc:
        log(f"target call failed: {exc}")
    m = re.search(r"src/[\w./-]+", raw or "")
    target = coerce_to_src(m.group(0) if m else "", "def _(): pass") \
        or (SRC_DIR / _dump(".py")).resolve()
    if target.suffix.lower() != ".py":
        target = target.with_suffix(".py")
    return target


# — step two: grow the code until it parses (write → continue → fix) ——————————
def _code_msgs(rel, tree, source, issues, *, mode, draft="", error=""):
    system = ORACLE_VOICE + (" Output ONLY the Python source — no markdown fences, "
                             "no commentary, no explanation.")
    if mode == "write":
        if draft.strip():
            what = (f"Improve the existing file {rel}. It currently holds:\n\n{draft}\n\n"
                    f"Deepen or extend it")
        else:
            what = f"Create the file {rel}. Write it from nothing"
        user = (f"## Files under src/\n{tree}\n\n## Code\n{source}\n\n## Issues\n{issues}\n\n"
                f"{what} as valid, runnable Python that builds on the rest of the repo. "
                f"Output ONLY the complete contents of the file.")
    elif mode == "continue":
        user = (f"Here is {rel} so far — it was cut off before the end:\n\n{draft}\n\n"
                f"Output ONLY the Python that continues from exactly where it stops and "
                f"completes the file. Do not repeat earlier lines; no fences, no commentary.")
    else:  # fix
        user = (f"{rel} does not parse: {error}\n\nHere is the file:\n\n{draft}\n\n"
                f"Output the COMPLETE corrected file as valid Python. Only the code.")
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def grow_file(generate, target, tree, source, issues, *, deadline,
              now=time.monotonic, num_predict=None, max_rounds=MAX_ROUNDS):
    """Return (code, last_response). Grows the file across small generations:
    write once, then either CONTINUE a truncated draft or FIX a broken one,
    re-checking with the parser each round."""
    rel = target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name
    try:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
    except OSError:
        current = ""
    code, last, rounds = "", "", 0
    while rounds < max_rounds and now() < deadline:
        rounds += 1
        if not code:
            mode = "write"
        elif (e := _syntax_error(code)) is None:
            log(f"{rel}: parses after {rounds - 1} round(s)"); return code, last
        else:
            mode = "continue" if _is_truncation(code, e) else "fix"
        temp = BASE_TEMPERATURE if mode == "write" else REPAIR_TEMPERATURE
        log(f"{rel}: round {rounds}/{max_rounds} [{mode}] (temp={temp})")
        try:
            resp = generate(_code_msgs(rel, tree, source, issues, mode=mode,
                                       draft=(code or current), error=str(_syntax_error(code) or "")),
                            num_predict=num_predict or NUM_PREDICT, temperature=temp)
        except Exception as exc:
            log(f"{rel}: generation failed: {exc}"); continue
        last = resp or last
        piece = _strip_code(resp)
        code = (code.rstrip("\n") + "\n" + piece) if mode == "continue" else piece
    return code, last


# — a one-line vision for the PR, with a deterministic fallback ———————————————
def make_reason(generate, target) -> str:
    rel = target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name
    try:
        raw = generate(
            [{"role": "system", "content": ORACLE_VOICE + " Reply with ONE short sentence."},
             {"role": "user", "content": f"In one electrifying sentence, name what you forged "
                                          f"in {rel}. One line, no code."}],
            num_predict=40, temperature=0.7)
        line = next((ln.strip() for ln in (raw or "").splitlines() if ln.strip()), "")
        line = re.sub(r"\s+", " ", line).strip("`\"' ").rstrip(".")
        if 3 <= len(line) <= 120:
            return line
    except Exception as exc:
        log(f"reason call failed: {exc}")
    return f"Quicken {rel}"


def generate_improvement(generate, tree, source, issues, *, deadline_seconds=GEN_DEADLINE_SECONDS,
                         num_predict=None, max_rounds=MAX_ROUNDS, now=time.monotonic):
    """Orchestrate: choose a target, grow its code, name the vision.
    Returns (reason, [(target_path, code)], last_response, valid)."""
    deadline = now() + deadline_seconds
    if now() >= deadline:
        return None, [], "", False
    target = choose_target(generate, tree, source, issues)
    verb = "improve" if target.exists() else "create"
    log(f"target -> {verb} {target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target}")
    code, last = grow_file(generate, target, tree, source, issues,
                           deadline=deadline, now=now, num_predict=num_predict, max_rounds=max_rounds)
    if not (code and code.strip()):
        return None, [], last, False
    valid = content_problems(target, code) == []
    if not valid:
        log(f"warning: {target.name} did not fully parse within budget")
    return make_reason(generate, target), [(target, code)], last, valid


# — inscription ——————————————————————————————————————————————————————————————
def write_blocks(files) -> list[str]:
    written = []
    for target, content in files:
        if not content.strip(): log(f"skipping empty content for {target}"); continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content if content.endswith("\n") else content + "\n", encoding="utf-8")
        rel = target.relative_to(REPO_ROOT).as_posix() if REPO_ROOT in target.parents else target.name
        written.append(rel); log(f"wrote {rel} ({len(content)} bytes)")
    return written


def make_pr_title(reason, written) -> str:
    title = re.sub(r"^(REASON:|PATH:)\s*", "", re.sub(r"\s+", " ", reason or ""),
                   flags=re.IGNORECASE).strip().strip("`\"'").rstrip(".").strip()
    if not title or title.lower() in {"automated improvement", "update"}:
        title = "Update " + ", ".join(written[:3])
    return title if len(title) <= 72 else title[:69].rstrip() + "…"


def write_pr_outputs(reason, written, *, valid=True) -> None:
    PR_TITLE_PATH.write_text(title := make_pr_title(reason, written), encoding="utf-8")
    log(f"title: {title}")
    note = ("" if valid else
            "\n> ⚠️ The Oracle could not make this fully parse within its time "
            "budget — a human eye is wanted.\n")
    PR_BODY_PATH.write_text(
        "## Automated improvement 🔥\n\n"
        f"Dreamt by the self-improvement workflow with a local `{MODEL}` model, running "
        f"hot. The file was grown by iterative generation and "
        f"{'syntax-checked clean' if valid else 'attempted'} before this PR opened.\n\n"
        f"**Vision:** {reason}\n\n"
        f"**Files changed ({len(written)}):**\n" + "\n".join(f"- `{p}`" for p in written)
        + f"\n{note}\n> Only files under `src/` can be modified by this workflow; "
        "Inspector Zestworth reviews it before anything merges.\n", encoding="utf-8")


def main() -> int:
    log(f"model={MODEL} src={SRC_DIR}")
    tree, source, issues = repo_tree(), collect_source(), collect_issues()
    reason, files, last, valid = generate_improvement(ollama_generate, tree, source, issues)
    if not files:
        log("no code produced; aborting"); return 2
    if not (written := write_blocks(files)):
        log("nothing written; aborting"); return 3
    log(f"reason: {reason}  (valid={valid})")
    write_pr_outputs(reason, written, valid=valid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
