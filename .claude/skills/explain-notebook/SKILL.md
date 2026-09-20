---
name: explain-notebook
description: Use when writing or updating an explain.ipynb for a hard problem in this repo - what belongs in the notebook rather than the README.
---

# Explanation notebooks

Reserve `explain.ipynb` for problems where the *derivation* is the hard part.
Anything that fits in a README paragraph stays in the README.

## Structure

1. Title, problem link, one sentence on what the notebook adds.
2. Setup cell — resolve the project root from `Path.cwd()` upwards rather than
   assuming a working directory, since PyCharm and `jupyter lab` disagree about
   it:

   ```python
   ROOT = next(p for p in [pathlib.Path.cwd(), *pathlib.Path.cwd().parents] if (p / 'lc').is_dir())
   PROBLEM = ROOT / 'problems' / 'NNNN-slug'
   sys.path.insert(0, str(ROOT))
   solutions = load_solutions(PROBLEM)
   ```

   Never redefine the solutions in the notebook; import them so the notebook
   cannot drift from the tested code. Every later cell refers to `PROBLEM`, not
   to a relative path.
3. **The identity or invariant**, in LaTeX when it is a formula.
4. **A trace cell** — print the state the argument talks about, step by step, on
   a small input. The trace is the reason the notebook exists; a wall of prose
   is not.
5. Why the optimization is *allowed* (what the fast approach gets to skip
   knowing, and why that is safe).
6. Complexity table, and a pointer to `uv run lc bench <number>` for measured
   numbers.

## Rules

- Notebooks must run top to bottom against the current `solutions.py`:
  `uv run jupyter nbconvert --to notebook --execute --stdout problems/<dir>/explain.ipynb`
- Commit them with outputs cleared — `uv run lc nb` (see
  `.claude/rules/notebooks.md`). Any number worth keeping goes into the problem
  README, since the committed notebook shows none.
- Link the notebook from the problem README's Approaches section.
