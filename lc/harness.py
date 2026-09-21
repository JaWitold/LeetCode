"""Loading and running problem solutions.

A problem directory holds ``solutions.py`` with one or more ``Solution*``
classes, all implementing the same entry method.  A sibling ``test_*.py``
declares the cases; ``conftest.py`` crosses the two.
"""

from __future__ import annotations

import copy
import importlib.util
import inspect
import sys
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

SOLUTION_PREFIX = "Solution"


def problem_dir(anchor: str | Path) -> Path:
    """Directory of the problem that ``anchor`` (usually ``__file__``) lives in."""
    path = Path(anchor).resolve()
    return path if path.is_dir() else path.parent


def load_module(path: Path) -> ModuleType:
    """Import a file under a name unique to its problem directory."""
    name = f"lc_problem_{path.parent.name.replace('-', '_')}_{path.stem}"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_solutions(anchor: str | Path) -> list[type]:
    """Every ``Solution*`` class defined in the problem's ``solutions.py``.

    Ordered as written in the file, so the first one is the reference.
    """
    module = load_module(problem_dir(anchor) / "solutions.py")
    classes = [
        obj
        for name, obj in vars(module).items()
        if inspect.isclass(obj)
        and name.startswith(SOLUTION_PREFIX)
        and obj.__module__ == module.__name__
    ]
    if not classes:
        raise RuntimeError(f"no {SOLUTION_PREFIX}* class in {module.__file__}")
    return classes


def entry(solution: type) -> Callable[..., Any]:
    """The method to call on a solution instance.

    Uses ``ENTRY = "twoSum"`` in ``solutions.py`` when present, otherwise the
    single public method on the class.
    """
    module = sys.modules[solution.__module__]
    name = getattr(module, "ENTRY", None)
    if name is None:
        methods = [n for n, m in vars(solution).items() if not n.startswith("_") and callable(m)]
        if len(methods) != 1:
            raise RuntimeError(
                f"{solution.__name__} has {len(methods)} public methods; set ENTRY in solutions.py"
            )
        name = methods[0]
    return getattr(solution(), name)


def default_equal(expected: Any, actual: Any) -> bool:
    return expected == actual


class Comparison:
    """How a module wants its results compared.

    ``normalize`` is the useful half: when a module defines ``NORMALIZE``, both
    sides are put through it and compared with a plain ``==``, so pytest's
    assertion rewriting produces a real diff of the normalized values. A module
    that defines ``EQUAL`` instead gets its predicate called, which no longer
    yields a diff — prefer ``NORMALIZE`` where the answer has a canonical form.
    """

    def __init__(
        self,
        equal: Callable[[Any, Any], bool] = default_equal,
        normalize: Callable[[Any], Any] | None = None,
    ) -> None:
        self.equal = equal
        self.normalize = normalize

    def __repr__(self) -> str:
        if self.normalize is not None:
            return f"Comparison(normalize={self.normalize.__name__})"
        if self.equal is not default_equal:
            return f"Comparison(equal={self.equal.__name__})"
        return "Comparison(==)"

    def __call__(self, expected: Any, actual: Any) -> bool:
        if self.normalize is not None:
            return self.normalize(expected) == self.normalize(actual)
        return self.equal(expected, actual)


@dataclass(frozen=True)
class Case:
    args: tuple[Any, ...]
    expected: Any

    @property
    def id(self) -> str:
        text = ", ".join(repr(a) for a in self.args)
        return text if len(text) <= 40 else text[:37] + "..."


def as_cases(raw: Iterable[Any]) -> list[Case]:
    """Normalize a ``CASES`` list into ``Case`` objects.

    Each entry is ``(args_tuple, expected)``; a lone non-tuple argument may be
    written bare.  ``expected`` may be a callable ``(actual, *args) -> bool``
    for problems with several valid answers.
    """
    cases = []
    for item in raw:
        if isinstance(item, Case):
            cases.append(item)
            continue
        args, expected = item
        if not isinstance(args, tuple):
            args = (args,)
        cases.append(Case(args, expected))
    return cases


def invoke(solution: type, case: Case) -> tuple[Any, tuple[Any, ...]]:
    """Call ``solution`` on ``case``.

    Arguments are deep-copied per run, so a solution may mutate them without
    corrupting the shared case.  Returns the result *and* the copies it was
    given, which is what makes in-place answers checkable.
    """
    args = copy.deepcopy(case.args)
    return entry(solution)(*args), args


def run(solution: type, case: Case) -> Any:
    """The return value alone; see :func:`invoke` for in-place inspection."""
    return invoke(solution, case)[0]


def call_repr(solution: type, case: Case) -> str:
    method = getattr(sys.modules[solution.__module__], "ENTRY", "solve")
    return f"{solution.__name__}.{method}({case.id})"


def bind(solution: type, args: tuple[Any, ...]) -> dict[str, Any]:
    """Arguments by parameter name, as the solution's own signature names them."""
    bound = inspect.signature(entry(solution)).bind(*args)
    return dict(bound.arguments)


class After:
    """Expectation on the arguments a solution mutated in place.

    ``after(nums=[1, 3, 12, 0, 0])`` asserts on ``nums`` once the call
    returned, by the parameter name in the solution's signature.  Pass
    ``returns=`` to also pin the return value (LeetCode's in-place problems
    usually return a length), and give any expectation as a callable
    ``(actual) -> bool`` to check it loosely.
    """

    IGNORE = object()

    def __init__(self, *, returns: Any = IGNORE, **arguments: Any) -> None:
        if not arguments:
            raise ValueError("after() needs at least one argument expectation")
        self.returns = returns
        self.arguments = arguments

    def __repr__(self) -> str:
        parts = [f"{k}={v!r}" for k, v in self.arguments.items()]
        if self.returns is not After.IGNORE:
            parts.append(f"returns={self.returns!r}")
        return f"after({', '.join(parts)})"

    def verify(self, solution: type, case: Case, result: Any, args: tuple[Any, ...]) -> None:
        __tracebackhide__ = True
        call = call_repr(solution, case)
        bound = bind(solution, args)
        for name, expected in self.arguments.items():
            if name not in bound:
                raise RuntimeError(f"{call} has no parameter {name!r}; it takes {', '.join(bound)}")
            actual = bound[name]
            if callable(expected):
                assert expected(actual), f"{call} left {name} = {actual!r}, rejected by validator"
            else:
                assert actual == expected, f"{call} left {name} ="
        if self.returns is not After.IGNORE:
            assert result == self.returns, f"{call} returned"


def after(**kwargs: Any) -> After:
    """Sugar for :class:`After`; see its docstring."""
    return After(**kwargs)


def check(solution: type, case: Case, equal: Callable[[Any, Any], bool] = default_equal) -> None:
    """Run one case and assert on it, hiding this frame from the traceback."""
    __tracebackhide__ = True
    result, args = invoke(solution, case)
    expected = case.expected
    call = call_repr(solution, case)

    normalize = getattr(equal, "normalize", None)

    if isinstance(expected, After):
        expected.verify(solution, case, result, args)
    elif callable(expected) and not isinstance(expected, type):
        assert expected(result, *args), (
            f"{call}\n  returned: {result!r}\n  rejected by the case's validator"
        )
    elif normalize is not None:
        # normalize both sides, then compare plainly so pytest can diff them
        assert _normalized(normalize, result, call) == normalize(expected), (
            f"{call} returned, normalized:"
        )
    elif equal is default_equal or getattr(equal, "equal", None) is default_equal:
        # plain comparison so pytest rewrites it into a real expected/actual diff
        assert result == expected, f"{call} returned:"
    else:
        try:
            verdict = equal(expected, result)
        except Exception as exc:
            raise AssertionError(
                f"{call}\n  returned: {result!r}"
                f"\n  which the module's EQUAL could not handle: {type(exc).__name__}: {exc}"
            ) from None
        assert verdict, (
            f"{call}\n  returned: {result!r}\n  expected: {expected!r}"
            f"\n  compared with the module's EQUAL"
        )


def _normalized(normalize: Callable[[Any], Any], result: Any, call: str) -> Any:
    """Normalize a result, reporting a bad result rather than the normalizer's crash."""
    __tracebackhide__ = True
    try:
        return normalize(result)
    except Exception as exc:
        hint = " — a solution with no return statement returns None" if result is None else ""
        raise AssertionError(
            f"{call}\n  returned: {result!r}"
            f"\n  which NORMALIZE could not handle: {type(exc).__name__}: {exc}{hint}"
        ) from None
