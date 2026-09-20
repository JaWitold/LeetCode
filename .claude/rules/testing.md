# Testing

- Test modules declare data, not logic: `SOLUTIONS = load_solutions(__file__)`,
  a `CASES` list, and the three-line `test_solution` body. Root `conftest.py`
  parametrizes every solution against every case, so a new approach needs no
  new test code. If a test module needs a hand-written assertion, that is a sign
  the harness should grow instead.
- A case is `(args_tuple, expected)`. A single non-tuple argument may be bare.
  `expected` is one of:
  - a value, compared against the return value;
  - `after(nums=[1, 3, 12, 0, 0])` for solutions that answer **in place** —
    arguments are named as the solution's own signature names them, checked
    after the call, and `returns=` additionally pins the return value (the `k`
    of the remove/partition problems). Any expectation there may itself be a
    callable `(actual) -> bool`;
  - a callable `(actual, *args) -> bool` for problems with several valid
    answers, where `args` are the arguments *as the solution left them*.
  For a loose comparison across every case in a module, define
  `EQUAL(expected, actual)` there instead.
- Arguments are deep-copied per run, so solutions may mutate freely and cases
  are never shared between approaches.
- Failures print `Solution.method(args)` followed by pytest's own
  expected/actual diff; `lc.harness` is assertion-rewritten in `conftest.py` to
  make that work, so keep the asserts in `check` as plain comparisons.
- Cases are written before the solution and must include the problem's own
  examples, the boundaries the constraints permit (empty, single, all-equal,
  extremes of sign and value), and at least one input big enough to make the
  benchmark meaningful.
- Test file names must be unique across the repo (`test_<slug>.py`), since
  pytest imports them into one namespace.
- `uv run pytest -k <SolutionName>` runs one approach; `-k <case id>` runs one
  case. Case ids are the repr of the arguments.
