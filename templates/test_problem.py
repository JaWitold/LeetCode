"""Cases for {{number}}. {{title}}.

Declare data only: ``conftest.py`` parametrizes over SOLUTIONS x CASES.
"""

from lc.harness import after, check, load_solutions  # noqa: F401

SOLUTIONS = load_solutions(__file__)

# (args_tuple, expected)
#   expected = a value                 -> compared against the return value
#   expected = after(nums=[...])       -> compared against an argument mutated in place,
#                                         optionally with returns=<value>
#   expected = lambda actual, *args    -> free-form check, for several valid answers
#
# Answer order not fixed? define NORMALIZE(value) here and both sides are put
# into canonical form before comparing, keeping pytest's diff on failure.
CASES = [
]


def test_solution(solution, case, equal):
    check(solution, case, equal)
