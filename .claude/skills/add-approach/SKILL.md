---
name: add-approach
description: Use when adding a second or faster solution to an existing problem in this repo, or when asked to optimize a solution.
---

# Adding an approach

Never replace an existing `Solution*` class with a faster one. Add a new class
to the same `solutions.py`; `conftest.py` picks it up and runs it against every
existing case with no new test code.

1. Name it for the technique, not the ranking: `SolutionTwoPointers`,
   `SolutionMonotonicStack`, `SolutionBinarySearch` — not `SolutionOptimized`
   or `SolutionV2`.
2. Class docstring states the invariant that makes the shortcut legal, then
   time and space on the last line. The invariant is the part worth keeping.
3. `uv run pytest problems/<dir>` — all approaches, all cases.
4. `uv run lc bench <number>` and record the ranking in the README only when the
   measurement is surprising (a "better" complexity losing on the case sizes at
   hand is worth a note).
5. Add a subsection to the README's Approaches and rerun `uv run lc index`.

If the new approach needs a case the current `CASES` do not cover — the
adversarial input that breaks the naive one — add that case first and confirm
the old solution still passes it.
