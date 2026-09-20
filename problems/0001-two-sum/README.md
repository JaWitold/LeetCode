---
number: 1
title: Two Sum
difficulty: easy
topics: junior, array, hash-table
url: https://leetcode.com/problems/two-sum/
status: solved
---

# 1. Two Sum

## Problem

You are given an array of integers `nums` and an integer `target`, return
indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not
use the same element twice.

You can return the answer in any order.

**Example 1:**

```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

**Example 2:**

```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

**Example 3:**

```
Input: nums = [3,3], target = 6
Output: [0,1]
```

**Constraints:**

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Only one valid answer exists.

## Approaches

All four search the same space; they differ in *who* does the searching — the
interpreter, the C implementation of `list`, or a hash table.

| Approach | Time | Space | LeetCode runtime |
|---|---|---|---|
| `SolutionNestedLoops` | O(n²) | O(1) | 1745 ms |
| `SolutionNestedLoopsSkipRepeats` | O(n²) | O(n) | 1555 ms |
| `SolutionComplementScan` | O(n²) | O(1) | 355 ms |
| `SolutionComplementHashMap` | O(n) | O(n) | 4 ms |

Local `uv run lc bench 1` agrees with that ordering: 16x, 81x and 95x slower
than the hash map respectively.

### SolutionNestedLoops

Try every pair in index order. The baseline.

- **Time:** O(n²) — every pair is examined in the worst case
- **Space:** O(1) — two indices

### SolutionNestedLoopsSkipRepeats

The same loops, except a value that has already served as the left element is
skipped. That is safe: any partner of a *later* occurrence also sits to the
right of the *first* occurrence, so the first pass would have found that pair
already.

It only helps on inputs with many duplicates, and it buys that with O(n) space
for the set of seen values — the one correction to make against the earlier
note, which claimed O(1). The measured gain over the plain loops is small.

- **Time:** O(n²) — unchanged; all-distinct input skips nothing
- **Space:** O(n) — the set of values already used as the left element

### SolutionComplementScan

Still a quadratic search, but the inner loop is delegated to
`nums.index(target - value, i + 1)`. No set is involved despite the name of the
first draft — `list.index` is a linear scan, just one that runs in C rather than
in the interpreter.

So the complexity is unchanged and only the constant factor drops, which is why
it is ~5x faster on LeetCode while still losing badly to the hash map. `except
ValueError` (not a bare `except`) is what keeps a genuine bug from being
swallowed here.

- **Time:** O(n²) — `list.index` is a linear scan, run once per element
- **Space:** O(1) — the scan allocates nothing

### SolutionComplementHashMap

One pass. At index `i` the map holds `target - nums[j] -> j` for every `j < i`,
so `nums[i] in seen` means "an earlier element is waiting for exactly this
value" and the answer is `[seen[nums[i]], i]`.

Two details carry the correctness:

- storing **after** the look-up, which is what stops an element from pairing
  with itself;
- keying by the complement rather than by the value, so the check is a single
  hash lookup instead of an arithmetic step plus a lookup. Keying by the value
  and looking up `target - nums[i]` is equivalent — same complexity, same
  invariant.

- **Time:** O(n) — one pass, each look-up and insert amortized O(1)
- **Space:** O(n) — the map holds at most one entry per element seen

The low "memory beats" percentage is the price of the dictionary and is
expected; the runtime column is the one that matters here.

See [`explain.ipynb`](explain.ipynb) for the measurements and why the C-level
scan sits between the two complexity classes.

## Edge cases

The cases in `test_two_sum.py` guard:

- the pair being a repeated value (`[3, 3]`) — catches a solution that pairs an
  element with itself, i.e. storing into the map before the look-up;
- repeats that are *not* the answer (`[5, 5, 5, 2, 7]`) — catches an
  over-eager skip in `SolutionNestedLoopsSkipRepeats`;
- negatives and zeros (`[0, 4, 3, 0]`, target `0`) — catches treating a falsy
  value as "absent";
- the answer at the far end of a 1000-element array — the only case where the
  runtime difference between the approaches is visible.

## Notes

- "Better complexity" and "faster" are different claims. `SolutionComplementScan`
  is quadratic and still beats a quadratic interpreter loop by 5x, because the
  work moved into C. On LeetCode-sized inputs the constant factor decides a lot
  of easy problems.
- The dictionary trick — store what you are *waiting for*, look up what you
  *have* — carries over to [15. 3Sum](https://leetcode.com/problems/3sum/) and
  [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
  (where a sorted input allows two pointers and O(1) space instead).
- LeetCode's "Beats %" is noisy between submissions of identical code; the
  absolute millisecond figures are the more useful record.
