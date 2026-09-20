"""Locating problem directories."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "problems"
DIR_RE = re.compile(r"^(\d{4})-([a-z0-9-]+)$")


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def all_problems() -> list[Path]:
    if not PROBLEMS.is_dir():
        return []
    return sorted(p for p in PROBLEMS.iterdir() if p.is_dir() and DIR_RE.match(p.name))


def find(ref: str) -> Path:
    """Resolve ``42``, ``0042``, ``trapping-rain-water`` or a path to a problem dir."""
    candidate = Path(ref)
    if candidate.is_dir() and (candidate / "solutions.py").exists():
        return candidate.resolve()
    matches = []
    for path in all_problems():
        number, slug = DIR_RE.match(path.name).groups()
        if ref == path.name or ref == slug or ref.lstrip("0") == number.lstrip("0"):
            matches.append(path)
    if not matches:
        raise SystemExit(f"no problem matching {ref!r} under {PROBLEMS}")
    if len(matches) > 1:
        raise SystemExit(f"{ref!r} matches: {', '.join(p.name for p in matches)}")
    return matches[0]
