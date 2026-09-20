"""``lc index``: regenerate the progress table in the root README."""

from __future__ import annotations

from lc import meta
from lc.harness import load_solutions
from lc.paths import DIR_RE, ROOT, all_problems

START = "<!-- lc:index:start -->"
END = "<!-- lc:index:end -->"
HEADER = (
    "| # | Problem | Difficulty | Topics | Approaches | Notes |\n"
    "|---|---------|------------|--------|------------|-------|\n"
)


def _row(path) -> str:
    number, slug = DIR_RE.match(path.name).groups()
    info = meta.parse(path / "README.md")
    title = info.get("title", slug.replace("-", " ").title())
    link = f"[{title}]({path.relative_to(ROOT)}/README.md)"
    try:
        approaches = ", ".join(
            c.__name__.removeprefix("Solution") or "Solution" for c in load_solutions(path)
        )
    except Exception as exc:  # unfinished problem: keep the table rendering
        approaches = f"_{type(exc).__name__}_"
    notebook = "notebook" if (path / "explain.ipynb").exists() else ""
    return (
        f"| {int(number)} | {link} | {info.get('difficulty', '')} | "
        f"{info.get('topics', '')} | {approaches} | {notebook} |\n"
    )


def table() -> str:
    problems = all_problems()
    if not problems:
        return '_No problems yet. Run `uv run lc new 1 "Two Sum"`._\n'
    return HEADER + "".join(_row(p) for p in problems)


def rebuild() -> int:
    readme = ROOT / "README.md"
    text = readme.read_text()
    if START not in text or END not in text:
        raise SystemExit(f"README.md is missing the {START} / {END} markers")
    head, _, rest = text.partition(START)
    _, _, tail = rest.partition(END)
    readme.write_text(f"{head}{START}\n{table()}{END}{tail}")
    print(f"indexed {len(all_problems())} problems")
    return 0
