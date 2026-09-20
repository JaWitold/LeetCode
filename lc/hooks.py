"""``lc hooks``: point git at the repo's tracked hooks directory.

Hooks cannot be committed into ``.git/hooks``, so they live in ``.githooks/``
and git is told to look there — one config setting, versioned with the repo.
"""

from __future__ import annotations

import subprocess

from lc.paths import ROOT

HOOKS_DIR = ".githooks"


def run(*, uninstall: bool) -> int:
    if uninstall:
        subprocess.run(["git", "config", "--unset", "core.hooksPath"], cwd=ROOT, check=False)
        print("hooks disabled; git is back to .git/hooks")
        return 0
    subprocess.run(["git", "config", "core.hooksPath", HOOKS_DIR], cwd=ROOT, check=True)
    print(f"core.hooksPath = {HOOKS_DIR}; pre-commit runs lc nb --check, ruff and pytest")
    return 0
