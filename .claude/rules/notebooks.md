# Notebooks

**Commit notebooks with outputs cleared.** `uv run lc nb` strips them;
`uv run lc nb --check` fails when any are dirty, so it is the thing to run
before committing (and the check to wire into a hook or CI).

Why cleared:

- outputs turn every rerun into a diff — execution counts shuffle, ids change,
  and a one-line edit shows up as a rewritten file;
- these notebooks print *timings*, which differ per machine and per run. A
  committed 4.48 ms reads as a fact about the algorithm when it is a fact about
  the laptop that happened to run it;
- the numbers worth keeping are already written down, annotated, in the
  problem's `README.md` (the complexity and LeetCode-runtime table). That table
  is the durable record; the notebook is how it was derived.

Consequences to respect:

- The notebook must **run top to bottom against the current `solutions.py`**,
  because nobody can see stale outputs to notice it broke. Verify with
  `uv run jupyter nbconvert --to notebook --execute --stdout problems/<dir>/explain.ipynb`
  after touching either file.
- A number that matters goes into the README, not only into a cell's output.
- Cells must not depend on the working directory — resolve the project root
  from `Path.cwd()` upwards, as the template's setup cell does.

If a notebook ever needs its output committed (a plot that takes minutes to
produce, say), say so explicitly in the problem README and keep it the
exception.
