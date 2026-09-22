---
number: 17
title: Letter Combinations of a Phone Number
difficulty: medium
topics: hash-table, string, backtracking
url: https://leetcode.com/problems/letter-combinations-of-a-phone-number/
status: solved
---

# 17. Letter Combinations of a Phone Number

## Problem

Given a string containing digits from `2-9` inclusive, return all possible
letter combinations that the number could represent. Return the answer in
**any order**.

A mapping of digits to letters (just like on the telephone buttons) is given
below. Note that 1 does not map to any letters.

```
2 -> abc    3 -> def    4 -> ghi    5 -> jkl
6 -> mno    7 -> pqrs   8 -> tuv    9 -> wxyz
```

**Example 1:**

```
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

**Example 2:**

```
Input: digits = "2"
Output: ["a","b","c"]
```

**Constraints:**

- `1 <= digits.length <= 4`
- `digits[i]` is a digit in the range `['2', '9']`.

## Approaches

Both approaches are one recursion: the combinations for `digits` are every
letter of the first digit prefixed onto every combination of the rest. Written
as a comprehension it fits in four lines — and the only difference between the
two is the order of the two `for` clauses.

| # | Approach | Time | Space | LeetCode | Local, `"7979"` |
|---|----------|------|-------|----------|-----------------|
| 1 | `SolutionRecursiveSuffixPerLetter` | O(n²·4ⁿ) | O(4ⁿ) | 0 ms | 0.166 ms |
| 2 | `SolutionRecursiveSuffixOnce` | O(n·4ⁿ) | O(4ⁿ) | 0 ms | 0.027 ms |

Space is the answer itself; the recursion adds O(n) frames. With `n ≤ 4` the
answer is at most 256 strings, which is why both are 0 ms on the judge.

### SolutionRecursiveSuffixPerLetter

```python
for letter in keypad[digits[0]]
for suffix in self.letterCombinations(digits[1:])
```

A comprehension re-evaluates its **inner** iterable once per item of the outer
one. The recursive call is in the inner clause, so the entire tail is recomputed
from scratch for every letter of the head digit — the recursion tree branches
rather than running straight down.

- **Time:** O(n²·4ⁿ) — each level recomputes the level below it once per letter
- **Space:** O(4ⁿ) — the answer; O(n) of stack on top

### SolutionRecursiveSuffixOnce

```python
for suffix in self.letterCombinations(digits[1:])
for letter in keypad[digits[0]]
```

The same two clauses, swapped. The recursive call is now the outer iterable,
which a comprehension evaluates exactly once, so the recursion walks straight
down the string: one call per digit.

- **Time:** O(n·4ⁿ) — one pass per level, building each output string once
- **Space:** O(4ⁿ) — as above

The base case returning `[""]` rather than `[]` is the identity the recursion
needs: the tail of the last digit must contribute exactly one empty suffix to
prefix onto. It is unreachable from outside, since the constraints guarantee at
least one digit — but it would be wrong for a version of this problem that
accepts `""` and expects `[]`.

## Edge cases

The cases in `test_letter_combinations_of_a_phone_number.py` guard:

- the problem's own two examples;
- `"7"` and `"9"` on their own — the two **four-letter** keys, which a keypad
  built by assuming three letters per digit gets wrong;
- `"79"`, both four-letter keys combined;
- `"2345"`, the maximum length with three-letter keys (81 combinations);
- `"7979"`, maximum length *and* maximum branching, the largest answer the
  constraints allow (256 combinations).

Expected values were generated with `itertools.product` and written into the
file as literals, so nothing in the test module recomputes the answer. Order is
free, so `NORMALIZE` sorts both sides.

## Notes

- **The two differ by the order of two `for` clauses, and that is a complexity
  difference, not a style one.** A comprehension evaluates its inner iterable
  once per outer item. Putting the recursive call inside means recomputing the
  whole tail per letter: 341 recursive calls for four digits against 5, and
  87,381 against 9 at eight digits. Both are still 0 ms on the judge because
  `n ≤ 4` caps the answer at 256 strings — the judge cannot see the difference,
  and a local measurement can.
- **The keypad dict is rebuilt on every call, and what that costs depends
  entirely on the call count.** Lifting it to module scope is worth 2.31x for
  the branching approach, which builds it 341 times on `"7979"`, and 1.04x for
  the linear one, which builds it 5 times. Per-call setup is only worth
  attacking once you know how often the call happens — fixing the loop order
  first makes this optimization almost pointless.
- Two measurements in this problem came out wrong the first time and had to be
  redone with `timeit` and repeated runs: single-run timings at this scale
  (microseconds) vary by more than the effects being measured, and one of them
  reversed the ranking entirely.
- The loop variable was named `digit` while holding a *letter*. Worth renaming
  the moment a comprehension has two clauses — that is where a wrong name stops
  being cosmetic and starts hiding which loop is which.
