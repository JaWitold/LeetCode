"""Reading the small YAML-ish front matter at the top of each problem README."""

from __future__ import annotations

from pathlib import Path

FIELDS = ("number", "title", "difficulty", "topics", "url", "approaches", "status")


def parse(readme: Path) -> dict[str, str]:
    """Front matter as a flat dict; missing file or fences yields ``{}``."""
    if not readme.exists():
        return {}
    lines = readme.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    meta: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if _:
            meta[key.strip()] = value.strip()
    return meta
