"""Cases for 1. Two Sum.

Declare data only: ``conftest.py`` parametrizes over SOLUTIONS x CASES.
"""

from lc.harness import check, load_solutions

SOLUTIONS = load_solutions(__file__)

# (args_tuple, expected); expected may be a callable (actual, *args) -> bool
CASES = [
    (([2, 7, 11, 15], 9), [0, 1]),
    (([3, 2, 4], 6), [1, 2]),
    (([3, 3], 6), [0, 1]),  # the pair is a repeated value
    (([-1, -2, -3, -4, -5], -8), [2, 4]),  # negatives
    (([0, 4, 3, 0], 0), [0, 3]),  # zeros, and target reached by two of them
    (([5, 5, 5, 2, 7], 9), [3, 4]),  # repeats that are *not* the answer
    ((list(range(1000)), 1997), [998, 999]),  # answer at the far end
]


def test_solution(solution, case, equal):
    check(solution, case, equal)
