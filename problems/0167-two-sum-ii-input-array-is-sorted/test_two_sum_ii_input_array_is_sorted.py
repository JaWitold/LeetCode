"""Cases for 167. Two Sum II - Input Array Is Sorted.

Declare data only: ``conftest.py`` parametrizes over SOLUTIONS x CASES.

Answers are **1-indexed**, and every case respects the problem's guarantee of
exactly one solution as well as its value range (-1000..1000), so a solution
may rely on both.
"""

from lc.harness import check, load_solutions

SOLUTIONS = load_solutions(__file__)

# (args_tuple, expected)
CASES = [
    # the problem's own examples
    (([2, 7, 11, 15], 9), [1, 2]),
    (([2, 3, 4], 6), [1, 3]),
    (([-1, 0], -1), [1, 2]),
    (([3, 3], 6), [1, 2]),
    (([1, 1, 1, 2, 7], 9), [4, 5]),
    (([-5, -3, 0, 1, 8], 3), [1, 5]),
    (([1, 2, 3, 9, 10], 19), [4, 5]),
    (([1, 2, 50, 90], 3), [1, 2]),
    ((list(range(-1000, 0)) + [1000], 0), [1, 1001]),
    (([-500, -499] + list(range(2, 1001)), -999), [1, 2]),
    ((([-1] * 2998 + [1, 1]), 2), [2999, 3000]),
    # duplicates on the answering side: ~18M valid pairs, so the one-solution
    # guarantee does not hold and each approach picks a different one — the hash
    # map answers [3, 4], a two-pointer walk answers [3, 5998]. Assert the pair
    # is 1-indexed, ordered, in range and actually sums to the target.
    (
        ([-1, -1] + [1, 1] * 2998, 2),
        lambda actual, numbers, target: (
            1 <= actual[0] < actual[1] <= len(numbers)
            and numbers[actual[0] - 1] + numbers[actual[1] - 1] == target
        ),
    ),
    (([-1000, 1000], 0), [1, 2]),
    (([0, 0], 0), [1, 2]),
    (([-1000, 0, 1000], 0), [1, 3]),
    (([-4, -2, 0, 1, 2], -4), [1, 3]),
    (([-500, -499, 500, 1000], -999), [1, 2]),
    (([1, 2, 4, 8, 16], 12), [3, 4]),
    (([1, 1, 2, 2, 3, 3], 6), [5, 6]),
    (([1] * 1000 + [2, 3], 5), [1001, 1002]),
    (([-5] + [2] * 2000 + [7], 2), [1, 2002]),
    (([-7] + [0] * 3000 + [8], 1), [1, 3002]),
    (
        ([-1000] * 5000 + [1000] * 5000, 0),
        lambda actual, numbers, target: (
            1 <= actual[0] < actual[1] <= len(numbers)
            and numbers[actual[0] - 1] + numbers[actual[1] - 1] == target
        ),
    ),
]


def test_solution(solution, case, equal):
    check(solution, case, equal)
