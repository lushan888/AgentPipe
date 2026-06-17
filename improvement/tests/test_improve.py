"""Unit tests for the Oracle's deterministic machinery.

No real model: the generator's two model calls (choose a path, grow the code)
are driven by small scripted fakes so the loop's logic — path coercion,
truncation-vs-error classification, the write→continue→fix progression — is
exercised directly and fast. Real generation is covered in test_integration.py.
"""
from __future__ import annotations

import ast

from oracle import improve


# A fake model keyed on which step is asking (we control the prompt text, so
# this is test-side dispatch, not production parsing).
def oracle_fake(*, path="src/mechanism.py", write="", cont="", fix="", reason="A bold vision"):
    calls = []

    def generate(messages, *, num_predict=None, temperature=None):
        calls.append(messages)
        u = messages[-1]["content"]
        if "Existing Python modules" in u:             return path
        if "electrifying sentence" in u:               return reason
        if "continues from exactly where" in u:        return cont
        if "does not parse" in u:                      return fix
        return write

    generate.calls = calls
    return generate


BIG = 10 ** 9  # effectively no deadline for the fast unit loops


# --- path coercion -----------------------------------------------------------
def test_bare_directory_becomes_a_file(scratch):
    scratch()
    t = improve.coerce_to_src("src/", "print('x')")
    assert t is not None and t != improve.SRC_DIR and t.suffix == ".py"


def test_traversal_is_contained(scratch):
    scratch()
    assert improve.coerce_to_src("../../etc/passwd", "data").is_relative_to(improve.SRC_DIR)


def test_absolute_path_is_contained(scratch):
    scratch()
    assert improve.coerce_to_src("/etc/shadow", "data").is_relative_to(improve.SRC_DIR)


# --- content validation ------------------------------------------------------
def test_valid_python_passes(scratch):
    scratch()
    assert improve.content_problems(improve.SRC_DIR / "m.py", "def f():\n    return 1\n") == []


def test_broken_python_is_flagged(scratch):
    scratch()
    probs = improve.content_problems(improve.SRC_DIR / "m.py", "def f():\n    return +\n")
    assert len(probs) == 1 and "syntax error" in probs[0].lower()


def test_markdown_is_not_syntax_checked(scratch):
    scratch()
    assert improve.content_problems(improve.SRC_DIR / "notes.md", "def not python (((") == []


# --- code extraction (model wraps in fences despite instructions) ------------
def test_strip_code_fenced():
    assert improve._strip_code("```python\nX = 1\n```") == "X = 1"


def test_strip_code_dangling_open_fence():
    assert improve._strip_code("```python\nX = 1") == "X = 1"


def test_strip_code_raw():
    assert improve._strip_code("X = 1\n") == "X = 1"


# --- truncation vs. logic error ---------------------------------------------
def test_truncation_detected_for_unclosed_bracket():
    code = "x = [1, 2,"
    assert improve._is_truncation(code, improve._syntax_error(code))


def test_truncation_detected_for_unterminated_paren_midfile():
    code = "def f(start):\n    total = (start +"
    assert improve._is_truncation(code, improve._syntax_error(code))


def test_logic_error_is_not_truncation():
    code = "def f(:\n    return 1"   # malformed signature, complete file
    e = improve._syntax_error(code)
    assert e is not None and not improve._is_truncation(code, e)


# --- choose the target file (a separate, constrained call) -------------------
def test_choose_target_extracts_path(scratch):
    scratch({"src/mechanism.py": ""})
    t = improve.choose_target(lambda m, **k: "I shall forge src/mechanism.py today", "t", "s", "i")
    assert t.name == "mechanism.py" and t.is_relative_to(improve.SRC_DIR)


def test_choose_target_can_create_a_new_file(scratch):
    scratch({"src/mechanism.py": ""})
    t = improve.choose_target(lambda m, **k: "src/orrery.py", "t", "s", "i")
    assert t.name == "orrery.py" and not t.exists()   # a NEW module, created later by write
    assert t.is_relative_to(improve.SRC_DIR)


def test_choose_target_defaults_on_junk(scratch):
    scratch()
    t = improve.choose_target(lambda m, **k: "no path here!!", "t", "s", "i")
    assert t.suffix == ".py" and t.is_relative_to(improve.SRC_DIR)


def test_choose_target_forces_py_extension(scratch):
    scratch()
    t = improve.choose_target(lambda m, **k: "src/notes", "t", "s", "i")
    assert t.suffix == ".py"


# --- grow the code: write → continue (truncated) / fix (broken) --------------
def test_grow_file_valid_on_first_write(scratch):
    scratch()
    target = improve.SRC_DIR / "m.py"
    g = oracle_fake(write="VALUE = 42\n")
    code, last = improve.grow_file(g, target, "t", "s", "i", deadline=BIG, max_rounds=4)
    assert improve.content_problems(target, code) == []
    assert len(g.calls) == 1  # no repair needed


def test_grow_file_continues_a_truncated_draft(scratch):
    scratch()
    target = improve.SRC_DIR / "m.py"
    g = oracle_fake(write="def tooth_count(start=13):\n    total = (start +",
                    cont=" 1)\n    return total\n")
    code, last = improve.grow_file(g, target, "t", "s", "i", deadline=BIG, max_rounds=4)
    assert improve.content_problems(target, code) == []
    assert "return total" in code


def test_grow_file_fixes_a_broken_draft(scratch):
    scratch()
    target = improve.SRC_DIR / "m.py"
    g = oracle_fake(write="def f(:\n    return 1", fix="def f():\n    return 1\n")
    code, last = improve.grow_file(g, target, "t", "s", "i", deadline=BIG, max_rounds=4)
    assert improve.content_problems(target, code) == []
    # it took the FIX path (not continue), proving the classification routed correctly
    assert any("does not parse" in m[-1]["content"] for m in g.calls)


# --- orchestration -----------------------------------------------------------
def test_generate_improvement_end_to_end(scratch):
    scratch({"src/mechanism.py": ""})
    g = oracle_fake(path="src/mechanism.py", write="VALUE = 42\n", reason="Forge the back dial")
    reason, files, last, valid = improve.generate_improvement(g, "t", "s", "i", deadline_seconds=999)
    assert valid and len(files) == 1
    target, code = files[0]
    assert target.name == "mechanism.py" and code.strip() == "VALUE = 42"
    assert reason == "Forge the back dial"
    written = improve.write_blocks(files)
    ast.parse((improve.SRC_DIR / "mechanism.py").read_text())
    improve.write_pr_outputs(reason, written, valid=valid)
    assert improve.PR_TITLE_PATH.read_text().strip()
    assert "Vision" in improve.PR_BODY_PATH.read_text()


def test_generate_improvement_reports_invalid_when_unrepairable(scratch):
    scratch()
    # always-broken write, and continue/fix also broken → never parses
    g = oracle_fake(write="def f(:", fix="def f(:", cont="def f(:")
    reason, files, last, valid = improve.generate_improvement(
        g, "t", "s", "i", deadline_seconds=999, max_rounds=3)
    assert files and valid is False  # ships best effort, flagged not-valid


def test_deadline_guard_makes_no_model_calls():
    def boom(*a, **k):
        raise AssertionError("model called past deadline")
    clock = iter([0, 100])  # now()=0 sets deadline=50; next now()=100 is past it
    reason, files, last, valid = improve.generate_improvement(
        boom, "t", "s", "i", deadline_seconds=50, now=lambda: next(clock))
    assert files == [] and valid is False


# --- ollama_generate request construction (mocked socket) --------------------
def test_ollama_generate_builds_request_and_parses(monkeypatch):
    import json
    captured = {}

    class FakeResp:
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return json.dumps({"message": {"content": "the gear turns"}}).encode()

    def fake_urlopen(req, timeout=None):
        captured["url"] = req.full_url
        captured["body"] = json.loads(req.data)
        return FakeResp()

    monkeypatch.setattr(improve.urllib.request, "urlopen", fake_urlopen)
    out = improve.ollama_generate([{"role": "user", "content": "hi"}], temperature=0.4, num_predict=7)
    assert out == "the gear turns"
    assert captured["url"].endswith("/api/chat")
    assert captured["body"]["options"]["num_predict"] == 7
