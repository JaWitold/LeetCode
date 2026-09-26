---
number: 36
title: Valid Sudoku
difficulty: medium
topics: array, hash-table, matrix
url: https://leetcode.com/problems/valid-sudoku/
status: solved
---

# 36. Valid Sudoku

## Problem

Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be
validated according to the following rules:

1. Each row must contain the digits `1-9` without repetition.
2. Each column must contain the digits `1-9` without repetition.
3. Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9`
   without repetition.

Note:

- A Sudoku board (partially filled) could be valid but is not necessarily
  solvable.
- Only the filled cells need to be validated according to the mentioned rules.

**Example 1:**

```
Input: board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true
```

**Example 2:**

```
Input: board =
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner
being modified to 8. Since there are two 8's in the top left 3x3 sub-box,
it is invalid.
```

**Constraints:**

- `board.length == 9`
- `board[i].length == 9`
- `board[i][j]` is a digit `1-9` or `.`.

## Approaches

Both make the same single pass over 81 cells and reject on the first repeat.
They differ only in what remembers the digits already seen.

| # | Approach | Time | Space | LeetCode | Local, solved board |
|---|----------|------|-------|----------|---------------------|
| 1 | `SolutionHashSet` | O(1) | O(1) | 2 ms, 19.31 MB | 14.5 µs |
| 2 | `SolutionBitmask` | O(1) | O(1) | 0 ms, 19.27 MB | 17.9 µs |

O(1) because the board is fixed at 9x9; in board width `n` both are O(n²) time,
and O(n²) space for the sets against O(n) for the integers.

### SolutionHashSet

One pass over all 81 cells. A digit is valid at `(r, c)` iff it hasn't been
seen yet in row `r`, column `c`, or box `(r // 3) * 3 + c // 3` — three
seen-sets, indexed as the cell is visited, reject on first repeat.

- **Time:** O(1) — the board is fixed at 9x9, so the single pass over 81
  cells is a constant; expressed in board width `n` it's O(n^2)
- **Space:** O(1) — 27 sets holding at most 9 digits each, likewise O(n) in
  board width `n`, excluding the input board itself

### SolutionBitmask

The same scan with each set replaced by the bits of one integer: digit `d` is
bit `d - 1`, so "seen it?" is `seen & mask` and "remember it" is `seen |= mask`.
Twenty-seven integers replace twenty-seven sets, and nothing is hashed or
allocated per cell.

- **Time:** O(1) — same 81-cell pass, with three bitwise tests per cell
- **Space:** O(1) — 27 integers regardless of how full the board is, and
  O(n) rather than O(n²) in board width `n`

**On the judge it wins: 0 ms against 2 ms. Locally it loses on a full board.**

| board | HashSet | Bitmask |
|---|---|---|
| fully solved, 81 clues | 14.5 µs | 17.9 µs |
| the example, 30 clues | 8.8 µs | 9.4 µs |
| empty board | 5.5 µs | 4.5 µs |
| invalid at cell (0,1) | 1.5 µs | 0.6 µs |

The reason is that the bitmask moves work *out* of C and into the interpreter.
Set membership on a one-character string is a C hash and compare; `1 << (ord(v)
- ord("1"))` is three interpreted bytecodes before the three `&` tests. Per 81
cells that arithmetic costs ~1.9 µs against ~1.5 µs for the set operations, and
replacing `ord` with a precomputed lookup table only recovers 0.8 µs of it.

Where it does win is when little work happens: an empty board allocates 27
integers instead of 27 sets, and an early rejection pays for almost nothing.
LeetCode's 507 cases are mostly small and mostly invalid, which is exactly that
regime — and at millisecond resolution 0 ms against 2 ms is the coarsest
possible view of a 3 µs difference.

## Edge cases

- `VALID_BOARD` / `BOX_DUPLICATE_BOARD` — the problem's own two examples;
  the second only differs in a box, so it also proves row/column checks
  alone aren't enough.
- `EMPTY_BOARD` — nothing filled in still must return `True`.
- `SINGLE_CELL_BOARD` — one digit, no peers to conflict with.
- `ROW_DUPLICATE_BOARD` / `COLUMN_DUPLICATE_BOARD` — duplicates placed far
  apart so they only share a row (or only a column), not a box.
- `SCATTERED_SAME_DIGIT_BOARD` — same digit repeated across the board but
  never sharing a row, column or box; catches an implementation that
  tracks "digit seen anywhere" instead of per-row/column/box.

## Notes

Box index `(r // 3) * 3 + c // 3` is the transferable trick — it's the same
flattening used for grid-of-blocks problems generally (image blur, tic-tac-toe
variants on bigger boards).

- **The bitmask is the textbook optimization and the slower program here.**
  Replacing a hash set with bit arithmetic is a clear win in C, where both are
  machine instructions and only one allocates. In CPython the set operation is
  already C and the arithmetic is not, so the "optimization" moves work in the
  wrong direction — 17.9 µs against 14.5 µs on a full board.
- **It still wins on the judge, for a reason that has nothing to do with being
  faster per cell.** LeetCode's 507 cases are dominated by small and invalid
  boards, where the bitmask's cheaper setup and earlier exit dominate, and the
  judge reports at millisecond resolution: 0 ms against 2 ms is a 3 µs
  difference rendered with a very blunt instrument.
- Worth remembering the general shape: in Python, an optimization that trades a
  C-implemented builtin for hand-written arithmetic usually loses, even when
  the operation count goes down.
