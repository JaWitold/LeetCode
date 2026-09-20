"""``lc new``: create a problem directory from the templates."""

from __future__ import annotations

from pathlib import Path

from lc import pycharm
from lc.paths import PROBLEMS, ROOT, slugify

TEMPLATES = ROOT / "templates"


def render(name: str, **values: str) -> str:
    text = (TEMPLATES / name).read_text()
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def create(
    *,
    number: int,
    title: str,
    difficulty: str,
    topics: list[str],
    entry: str,
    notebook: bool,
    run_config: bool = True,
) -> int:
    slug = slugify(title)
    target = PROBLEMS / f"{number:04d}-{slug}"
    if target.exists():
        raise SystemExit(f"{target} already exists")
    values = {
        "number": str(number),
        "title": title,
        "slug": slug,
        "difficulty": difficulty,
        "topics": ", ".join(topics),
        "url": f"https://leetcode.com/problems/{slug}/",
        "entry": entry or "solve",
        "module": slug.replace("-", "_"),
    }
    target.mkdir(parents=True)
    _write(target / "README.md", render("README.md", **values))
    _write(target / "solutions.py", render("solutions.py", **values))
    _write(target / f"test_{values['module']}.py", render("test_problem.py", **values))
    if notebook:
        _write(target / "explain.ipynb", render("explain.ipynb", **values))
    if run_config:
        pycharm.write(target)
    print(f"created {target.relative_to(ROOT)}")
    return 0


def _write(path: Path, text: str) -> None:
    path.write_text(text)
