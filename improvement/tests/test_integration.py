"""Integration tests that drive the ACTUAL local Ollama model.

Kept fast and bounded: tiny ``num_predict`` (the file is grown iteratively, so
small steps are fine), a short internal deadline, and a hard 60s per-test
timeout. The ``model`` fixture pulls the model if it isn't present; if no server
is reachable these skip.

    pdm run pytest -m integration -v
"""
from __future__ import annotations

import ast

import pytest

from oracle import improve

pytestmark = [pytest.mark.integration, pytest.mark.timeout(60)]

DEADLINE = 45   # internal soft budget — stays under the 60s hard timeout


def _ctx():
    return improve.repo_tree(), improve.collect_source(), "(no open issues)"


def test_real_choose_target_returns_a_py_path(model, quick_budget, scratch):
    scratch({"src/mechanism.py": "", "src/back_dial.py": ""})
    target = improve.choose_target(improve.ollama_generate, *_ctx())
    assert target.suffix == ".py" and target.is_relative_to(improve.SRC_DIR)


def test_real_generates_valid_python(model, quick_budget, scratch):
    scratch({"src/mechanism.py": "", "src/main.py": ""})
    tree, source, issues = _ctx()
    reason, files, last, valid = improve.generate_improvement(
        improve.ollama_generate, tree, source, issues, deadline_seconds=DEADLINE)
    assert files, f"no file produced; last response:\n{last[:400]}"
    target, code = files[0]
    assert target.suffix == ".py" and target.is_relative_to(improve.SRC_DIR)
    assert valid, f"{target.name} did not parse:\n{code[:400]}"
    ast.parse(code)


def test_real_writes_code_despite_a_distracting_recipe(model, quick_budget, scratch):
    """The regression empty-repo tests missed: an existing recipe used to derail
    the model into copying it. It must still produce valid Python."""
    scratch({
        "src/recipes/banana_pudding.md": "# Banana Pudding\n\nEggs, butter, bananas, milk...\n",
        "src/mechanism.py": "",
    })
    tree, source, issues = _ctx()
    reason, files, last, valid = improve.generate_improvement(
        improve.ollama_generate, tree, source, issues, deadline_seconds=DEADLINE)
    assert files, f"no file produced; last:\n{last[:400]}"
    target, code = files[0]
    assert target.suffix == ".py", f"wrote {target.name}, not Python"
    assert valid, f"{target.name} did not parse:\n{code[:400]}"
