"""``lc bench``: time each solution of a problem over its declared cases."""

from __future__ import annotations

import time
from pathlib import Path

from lc import harness
from lc.harness import as_cases, load_module, load_solutions
from lc.paths import find


def _cases(problem: Path) -> list:
    """Cases come from the problem's test module, so benchmarks never drift."""
    tests = sorted(problem.glob("test_*.py"))
    if not tests:
        raise SystemExit(f"no test module in {problem}")
    module = load_module(tests[0])
    raw = getattr(module, "CASES", None)
    if not raw:
        raise SystemExit(f"{tests[0]} declares no CASES")
    return as_cases(raw)


def run_problem(problem: Path, repeat: int) -> list[tuple[str, float]]:
    cases = _cases(problem)
    results = []
    for solution in load_solutions(problem):
        start = time.perf_counter()
        for _ in range(repeat):
            for case in cases:
                harness.run(solution, case)
        results.append((solution.__name__, time.perf_counter() - start))
    return results


def run(ref: str, *, repeat: int) -> int:
    problem = find(ref)
    results = run_problem(problem, repeat)
    baseline = min(t for _, t in results)
    width = max(len(name) for name, _ in results)
    print(f"{problem.name}  ({repeat} repeats)")
    for name, elapsed in sorted(results, key=lambda r: r[1]):
        per_run = elapsed / repeat * 1e6
        print(f"  {name:<{width}}  {per_run:8.1f} us/run   {elapsed / baseline:4.2f}x")
    return 0
