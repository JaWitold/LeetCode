"""Cases for 15. 3Sum.

The answer is a set of triplets: LeetCode accepts them in any order, and the
values inside one triplet in any order too. ``NORMALIZE`` puts both sides into
a canonical order before they are compared, so a case can be written in
whatever order reads best and a failure still shows a real diff.
"""

from lc.harness import check, load_solutions

SOLUTIONS = load_solutions(__file__)


def NORMALIZE(triplets):
    return sorted(sorted(triplet) for triplet in triplets)


CASES = [
    (([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]),
    (([0, 1, 1],), []),
    (([0, 0, 0],), [[0, 0, 0]]),
    (([0, 0, 0, 0],), [[0, 0, 0]]),
    (([1, 2, 3],), []),
    (([-1, -2, -3],), []),
    (([1, 2, 0, 1, 0, 0, 0, 0]), [[0, 0, 0]]),
    (([-2, 0, 1, 1, 2],), [[-2, 0, 2], [-2, 1, 1]]),
    (([-1, -1, -1, 2, 2, 2],), [[-1, -1, 2]]),
    (([-2, -1, 0, 1, 2],), [[-2, 0, 2], [-1, 0, 1]]),
    (([-4, -2, -2, 0, 2, 2, 4],), [[-4, 0, 4], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]),
    (([-100000, 50000, 50000],), [[-100000, 50000, 50000]]),
    (([-100000, 100000, 0, 100000],), [[-100000, 0, 100000]]),
    (([0] * 30,), [[0, 0, 0]]),
    (([2**i for i in range(1, 12)] + [-3072],), [[-3072, 1024, 2048]]),
    ((list(range(1, 301)),), []),
    ((list(range(-300, 0)),), []),
]


def test_solution(solution, case, equal):
    check(solution, case, equal)
