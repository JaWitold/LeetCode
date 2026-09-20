"""``lc nb``: strip notebook outputs, or verify they are already stripped."""

from __future__ import annotations

import json
from pathlib import Path

from lc.paths import ROOT


def notebooks() -> list[Path]:
    return sorted(
        p
        for p in ROOT.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in p.parts and ".venv" not in p.parts
    )


def strip(path: Path) -> bool:
    """Clear outputs and execution counts; returns True when the file changed."""
    original = path.read_text()
    notebook = json.loads(original)
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        cell["outputs"] = []
        cell["execution_count"] = None
        cell.get("metadata", {}).pop("execution", None)
    notebook.get("metadata", {}).pop("widgets", None)
    cleaned = json.dumps(notebook, indent=1) + "\n"
    if cleaned != original:
        path.write_text(cleaned)
        return True
    return False


def run(*, check: bool) -> int:
    dirty = []
    for path in notebooks():
        if check:
            notebook = json.loads(path.read_text())
            if any(
                cell.get("outputs") or cell.get("execution_count") is not None
                for cell in notebook.get("cells", [])
                if cell.get("cell_type") == "code"
            ):
                dirty.append(path)
        elif strip(path):
            dirty.append(path)
    if check and dirty:
        for path in dirty:
            print(f"has outputs: {path.relative_to(ROOT)}")
        print("run `uv run lc nb` before committing")
        return 1
    verb = "would strip" if check else "stripped"
    print(f"{verb} {len(dirty)} of {len(notebooks())} notebooks")
    return 0
