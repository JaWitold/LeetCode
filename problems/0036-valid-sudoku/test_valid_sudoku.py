"""Cases for 36. Valid Sudoku.

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
VALID_BOARD = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

# top-left box duplicate: 8 in [0][0] and [0][1] (LeetCode's own counterexample)
BOX_DUPLICATE_BOARD = [
    ["8", "8", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]

EMPTY_BOARD = [["." for _ in range(9)] for _ in range(9)]

SINGLE_CELL_BOARD = [["." for _ in range(9)] for _ in range(9)]
SINGLE_CELL_BOARD[4][4] = "5"

ROW_DUPLICATE_BOARD = [["." for _ in range(9)] for _ in range(9)]
ROW_DUPLICATE_BOARD[0][0] = "3"
ROW_DUPLICATE_BOARD[0][8] = "3"

COLUMN_DUPLICATE_BOARD = [["." for _ in range(9)] for _ in range(9)]
COLUMN_DUPLICATE_BOARD[0][0] = "3"
COLUMN_DUPLICATE_BOARD[8][0] = "3"

# same digit repeated across rows/columns but never sharing a row, column
# or box - only a naive "digit seen anywhere" check would reject this
SCATTERED_SAME_DIGIT_BOARD = [["." for _ in range(9)] for _ in range(9)]
SCATTERED_SAME_DIGIT_BOARD[0][0] = "7"
SCATTERED_SAME_DIGIT_BOARD[3][3] = "7"
SCATTERED_SAME_DIGIT_BOARD[6][6] = "7"

CASES = [
    (VALID_BOARD, True),
    (BOX_DUPLICATE_BOARD, False),
    (EMPTY_BOARD, True),
    (SINGLE_CELL_BOARD, True),
    (ROW_DUPLICATE_BOARD, False),
    (COLUMN_DUPLICATE_BOARD, False),
    (SCATTERED_SAME_DIGIT_BOARD, True),
]


def test_solution(solution, case, equal):
    check(solution, case, equal)
