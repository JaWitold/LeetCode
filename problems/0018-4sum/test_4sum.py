"""Cases for 18. 4Sum.

Like 3Sum, the answer is a set of tuples with no fixed order — neither between
quadruplets nor inside one — so ``NORMALIZE`` canonicalizes both sides before
they are compared.
"""

from lc.harness import check, load_solutions

SOLUTIONS = load_solutions(__file__)


def NORMALIZE(quadruplets):
    return sorted(sorted(quadruplet) for quadruplet in quadruplets)


CASES = [
    (([1, 0, -1, 0, -2, 2], 0), [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
    (([2, 2, 2, 2, 2], 8), [[2, 2, 2, 2]]),
    (([1], 0), []),
    (([1, 2, 3], 6), []),
    (([1, 2, 3, 4], 10), [[1, 2, 3, 4]]),
    (([1, 2, 3, 4], 11), []),
    (([0, 0, 0, 0, 0], 0), [[0, 0, 0, 0]]),
    (([0, 0, 0, 0, 1, 1, 1, 1], 2), [[0, 0, 1, 1]]),
    (([1, 1, 1, 1, 2, 2, 2, 2], 6), [[1, 1, 2, 2]]),
    (([-3, -1, 0, 2, 4, 5], 2), [[-3, -1, 2, 4]]),
    (([1, -2, -5, -4, -3, 3, 3, 5], -11), [[-5, -4, -3, 1]]),
    (([-2, -1, 0, 1, 2], 0), [[-2, -1, 1, 2]]),
    (
        ([-1000000000, -1000000000, 1000000000, 1000000000], 0),
        [[-1000000000, -1000000000, 1000000000, 1000000000]],
    ),
    ((list(range(1, 201)), 0), []),
    ((list(range(1, 201)), 10), [[1, 2, 3, 4]]),
    ((list(range(1, 201)), 794), [[197, 198, 199, 200]]),
]


def test_solution(solution, case, equal):
    check(solution, case, equal)
