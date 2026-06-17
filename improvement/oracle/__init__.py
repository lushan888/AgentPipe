"""The Oracle: an agentic self-improvement loop for the repository.

The Oracle reads the current state of ``src/``, dreams up a bold improvement,
and emits it as VALID code — repairing itself across sampling rounds until the
output parses. It only ever writes under ``src/``.
"""

from .improve import main

__all__ = ["main"]
