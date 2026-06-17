"""Shared fixtures.

The generation tests talk to a REAL local Ollama. The fixtures here find the
server, ensure the model is pulled (the first run may take a while), and point
the Oracle at a throwaway repo. If no server is reachable the integration tests
skip rather than fail.
"""
from __future__ import annotations

import json
import os
import urllib.request

import pytest

from oracle import improve

PULL_TIMEOUT = int(os.environ.get("IMPROVE_TEST_PULL_TIMEOUT", "1800"))


def _get(path, timeout=5):
    with urllib.request.urlopen(improve.OLLAMA_URL + path, timeout=timeout) as r:
        return json.load(r)


def _server_up() -> bool:
    try:
        _get("/api/version", timeout=3)
        return True
    except Exception:
        return False


def _installed() -> set[str]:
    try:
        return {m["name"] for m in _get("/api/tags").get("models", [])}
    except Exception:
        return set()


def _pull(model: str) -> None:
    body = json.dumps({"model": model, "stream": False}).encode()
    req = urllib.request.Request(
        improve.OLLAMA_URL + "/api/pull", data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=PULL_TIMEOUT) as r:
        r.read()  # blocks until the pull finishes


@pytest.fixture(scope="session")
def ollama_url() -> str:
    if not _server_up():
        pytest.skip(f"no Ollama server reachable at {improve.OLLAMA_URL}")
    return improve.OLLAMA_URL


@pytest.fixture(scope="session")
def model(ollama_url) -> str:
    """Ensure the model is available locally, pulling it if needed, and make the
    Oracle use it. Override with IMPROVE_TEST_MODEL (defaults to the prod model)."""
    name = os.environ.get("IMPROVE_TEST_MODEL", improve.MODEL)
    have = _installed()
    if name not in have and f"{name}:latest" not in have:
        _pull(name)
        assert name in _installed() or f"{name}:latest" in _installed(), \
            f"pull of {name!r} did not register in /api/tags"
    improve.MODEL = name  # so ollama_generate targets it
    return name


@pytest.fixture
def quick_budget(monkeypatch):
    """Tiny generation budget so real calls finish fast — the file is grown
    iteratively, so small steps are fine."""
    monkeypatch.setattr(improve, "NUM_PREDICT",
                        int(os.environ.get("IMPROVE_TEST_NUM_PREDICT", "256")))


@pytest.fixture
def scratch(tmp_path, monkeypatch):
    """Point improve.* at a fresh temp repo; return a factory to seed src/."""
    root = tmp_path
    (root / "src").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(improve, "REPO_ROOT", root.resolve())
    monkeypatch.setattr(improve, "SRC_DIR", (root / "src").resolve())
    monkeypatch.setattr(improve, "PR_BODY_PATH", root / "pr_body.md")
    monkeypatch.setattr(improve, "PR_TITLE_PATH", root / "pr_title.txt")

    def seed(files=None):
        for rel, body in (files or {}).items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
        return root

    return seed
