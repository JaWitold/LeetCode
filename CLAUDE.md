# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

A personal LeetCode practice repo: solutions, notes, tests and explanation
notebooks. The value is in the *comparison between approaches and the written
reasoning*, not in having one passing answer — treat notes and alternative
solutions as part of the deliverable, not extras.

## Commands

```bash
uv sync                                     # install dev tooling (pytest, ruff, jupyter)
uv run pytest                               # every problem
uv run pytest problems/NNNN-slug            # one problem
uv run pytest -k SolutionHashMap            # one approach, across all its cases
uv run lc new 704 "Binary Search" -d easy -t array,binary-search -e search [--notebook]
uv run lc bench 42 -r 500                   # time every approach of a problem
uv run lc index                             # regenerate the progress table in README.md
uv run lc pycharm                           # regenerate .idea run configurations for all problems
uv run lc nb [--check]                      # strip notebook outputs (commit them cleared)
uv run ruff format . && uv run ruff check .
uv run jupyter nbconvert --to notebook --execute --stdout problems/<dir>/explain.ipynb
```

`lc bench` and `lc new` accept a number (`42`), a slug (`trapping-rain-water`)
or a path.

## Architecture

Each problem is a self-contained directory `problems/NNNN-slug/` holding
`README.md` (front matter + notes), `solutions.py` (one `Solution*` class per
approach), `test_<slug>.py` (cases only) and optionally `explain.ipynb`.

The piece worth understanding is how those three files connect:

- `lc/harness.py` loads `solutions.py` by path under a name derived from the
  problem directory, so every problem can use the same file names without module
  collisions. `load_solutions` returns the `Solution*` classes in file order;
  `entry` resolves the method to call from module-level `ENTRY`; `invoke`
  deep-copies arguments and returns both the result and those copies, which is
  what lets `after(...)` assert on arguments an in-place solution mutated.
  `check` keeps its comparison a plain `assert a == b` and `conftest.py` calls
  `pytest.register_assert_rewrite("lc.harness")`, so a failure shows the real
  expected/actual diff instead of an opaque helper call.
- Root `conftest.py` is the crossing point: `pytest_generate_tests` parametrizes
  any test taking `solution` and `case` over the module's `SOLUTIONS` and
  `CASES`. **Consequence: adding an approach to `solutions.py` adds test
  coverage with no test edits.** Preserve that property — put shared behavior in
  the harness, not in per-problem test code.
- `lc/bench.py` reads `CASES` from the problem's *test module* rather than
  defining its own, so benchmarks can never drift from what is verified.
- `lc/index.py` regenerates the root README table between the `lc:index` markers
  from each problem's front matter plus its live `Solution*` classes; a problem
  whose `solutions.py` fails to import still renders a row.
- `templates/` feeds `lc new` via `{{placeholder}}` substitution and is excluded
  from ruff (the templates are not valid Python until rendered).
- `lc/pycharm.py` writes PyCharm run configurations into
  `.idea/runConfigurations/`; `lc new` adds one per problem (skip with
  `--no-run-config`). `.idea/` is git-ignored, so these are local scratch that
  `lc pycharm` rebuilds on any clone. `lc pycharm` regenerates them all and deletes stale ones,
  but only files carrying the generated-by marker — hand-made configurations
  are left alone.

## Workflow

Skills in `.claude/skills/` cover the recurring jobs — use them:
`new-problem` (scaffold through notes), `add-approach` (second/faster solution),
`explain-notebook` (when and how to write `explain.ipynb`).

Cases are written before solutions, and the first solution committed is the
straightforward one; optimizations arrive as additional classes so the tradeoff
stays visible. Run `uv run lc index` after anything that changes a problem's
front matter or its set of approaches.

@.claude/rules/solution-style.md
@.claude/rules/testing.md
@.claude/rules/notes.md
@.claude/rules/notebooks.md
@.claude/rules/git.md
