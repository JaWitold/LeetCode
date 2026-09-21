"""Crosses each problem's solutions with its cases.

A problem's ``test_*.py`` only declares data: ``SOLUTIONS`` (from
``load_solutions(__file__)``) and ``CASES``.  Every test taking a ``solution``
and/or ``case` argument is parametrized over them here, so adding a new
approach to ``solutions.py`` needs no new test code.  A module may also define
``EQUAL(expected, actual) -> bool`` to override comparison.
"""

from __future__ import annotations

import pytest

# harness.check does the asserting, so it needs rewriting to show expected/actual
pytest.register_assert_rewrite("lc.harness")

from lc.harness import Comparison, as_cases, default_equal  # noqa: E402


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    module = metafunc.module
    if "solution" in metafunc.fixturenames:
        solutions = getattr(module, "SOLUTIONS", None)
        if solutions:
            metafunc.parametrize("solution", solutions, ids=lambda s: s.__name__)
    if "case" in metafunc.fixturenames:
        raw = getattr(module, "CASES", None)
        if raw:
            cases = as_cases(raw)
            metafunc.parametrize("case", cases, ids=[c.id for c in cases])
        else:
            # freshly scaffolded problem: skip rather than error on a missing fixture
            skip = pytest.mark.skip(reason="no CASES declared yet")
            metafunc.parametrize("case", [pytest.param(None, marks=skip)])


@pytest.fixture
def equal(request: pytest.FixtureRequest) -> Comparison:
    """How this module compares results.

    ``NORMALIZE`` is preferred: both sides go through it and are compared with
    ``==``, so a failure shows pytest's own diff. ``EQUAL`` is the escape hatch
    for answers with no canonical form.
    """
    return Comparison(
        equal=getattr(request.module, "EQUAL", default_equal),
        normalize=getattr(request.module, "NORMALIZE", None),
    )
