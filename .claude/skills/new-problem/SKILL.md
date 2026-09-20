---
name: new-problem
description: Use when adding a LeetCode problem to this repo - scaffolds the directory, writes cases before solutions, and keeps notes and index in sync.
---

# Adding a problem

## Scaffold

```bash
uv run lc new <number> "<Title>" -d <easy|medium|hard> -t <topic,topic> -e <leetcodeMethodName> [--notebook]
```

This also drops a PyCharm run configuration into `.idea/runConfigurations/`
(pass `--no-run-config` to skip, `uv run lc pycharm` to rebuild them all).

`-e` must match the method name LeetCode gives, because the solution is pasted
back there. `--notebook` only for problems whose *idea* needs explaining — see
the `explain-notebook` skill.

## Then, in order

1. **README front matter and problem statement** — paste the statement from
   LeetCode verbatim, Constraints block included, and fix only styling and
   flattened superscripts (`104` -> `10^4`). Never reword it. Read the
   constraints before choosing an approach; they decide which complexity is
   acceptable.
2. **CASES before solutions.** Fill `CASES` in `test_<module>.py` with the
   examples from the problem plus the edge cases the constraints allow: empty
   input, single element, all-equal, extreme sign, and one input large enough to
   separate a quadratic approach from a linear one. Run `uv run pytest
   problems/<dir>` and watch them fail against the stub.
3. **Simplest correct solution first**, named for the technique
   (`SolutionBrute`, `SolutionSorting`, ...). Get it green.
4. **Optimize as a second class**, never by editing the first — the point of the
   repo is the comparison. See the `add-approach` skill.
5. **Fill the README approaches section** with the invariant that makes each one
   work, plus the mandatory time and space block (`- **Time:** O(n) — reason`)
   for every single solution, brute force included. "What would I need to re-derive this in six
   months?" is the bar.
6. `uv run lc index` and `uv run ruff format . && uv run ruff check .`

## Multiple valid answers

When the problem accepts several answers (any valid pair, any order), make
`expected` a callable `(actual, *args) -> bool` instead of a literal, or define
`EQUAL(expected, actual)` in the test module. Do not weaken the assertion by
sorting inside the solution.
