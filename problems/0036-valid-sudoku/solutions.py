"""36. Valid Sudoku — https://leetcode.com/problems/valid-sudoku/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.
"""

ENTRY = "isValidSudoku"


class SolutionSets:
    """
        O(1) time, O(1) space.

        Accepted
    507 / 507 testcases passed
    8VfDiH4dET
    8VfDiH4dET
    submitted at Sep 18, 2026 08:41

    Analysis

    Solution
    Runtime
    2
    ms
    Beats
    79.46%
    Memory
    19.31
    MB
    Beats
    36.93%
    """

    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for row in range(9):
            for col in range(9):
                box = 3 * (row // 3) + col // 3
                value = board[row][col]

                if value == ".":
                    continue

                if value in rows[row] or value in cols[col] or value in boxes[box]:
                    return False

                rows[row].add(value)
                cols[col].add(value)
                boxes[box].add(value)
        return True


class SolutionBin:
    """
        O(1) time, O(1) space.

        Runtime
    0
    ms
    Beats
    100.00%
    Memory
    19.27
    MB
    Beats
    75.62%

    """

    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9

        for row in range(9):
            for col in range(9):
                box = 3 * (row // 3) + col // 3
                value = board[row][col]

                if value == ".":
                    continue

                mask = 1 << (ord(value) - 49)
                if rows[row] & mask or cols[col] & mask or boxes[box] & mask:
                    return False

                rows[row] |= mask
                cols[col] |= mask
                boxes[box] |= mask
        return True
