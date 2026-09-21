---
number: 18
title: 4Sum
difficulty: medium
topics: array, two-pointers, sorting
url: https://leetcode.com/problems/4sum/
status: solved
---

# 18. 4Sum

## Problem

Given an array `nums` of `n` integers, return an array of all the **unique**
quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that:

- `0 <= a, b, c, d < n`
- `a`, `b`, `c`, and `d` are **distinct**.
- `nums[a] + nums[b] + nums[c] + nums[d] == target`

You may return the answer in **any order**.

**Example 1:**

```
Input: nums = [1,0,-1,0,-2,2], target = 0
Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
```

**Example 2:**

```
Input: nums = [2,2,2,2,2], target = 8
Output: [[2,2,2,2]]
```

**Constraints:**

- `1 <= nums.length <= 200`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`

## Approaches

[15. 3Sum](https://leetcode.com/problems/3sum/)'s answer with one more loop
around it: sort, pin the two smallest members, two-pointer the remaining
window, and jump the pointers with a binary search rather than stepping. The
two approaches here differ in one thing only — what collects the answer.

| # | Approach | Time | Space | LeetCode |
|---|----------|------|-------|----------|
| 1 | `SolutionBisectJumpSet` | O(n³) | O(t) | 8 ms |
| 2 | `SolutionBisectJumpList` | O(n³) | O(1) | 20 ms |

`t` is the size of the answer. Space excludes the output and the sort.

### SolutionBisectJumpSet

Pin `i` and `j`, two-pointer between `j + 1` and the end, collect into a set.

Four prunes ride on the sort, two per level: a pin whose smallest possible
partners already overshoot the target ends that loop, and one whose largest
possible partners still fall short is skipped. Those are what keep a cubic scan
practical at n = 200.

- **Time:** O(n³) — a two-pointer sweep for each of O(n²) pinned pairs
- **Space:** O(t) — one entry per quadruplet found

### SolutionBisectJumpList

The same scan, appending to a list.

- **Time:** O(n³) — as above
- **Space:** O(1) — three indices; the output is not counted

**The set in approach 1 never removes anything.** Every one of the four
positions steps over equal values — `i` and `j` skip repeats of the previous
pin, and `left`/`right` skip repeats after a hit — so each quadruplet is
reachable exactly once. Measured on 6000 random arrays, the list version emits
a duplicate in **zero** of them, and on a 200-element array with values in ±20
the two return byte-identical answers of a couple of thousand quadruplets.

## Edge cases

The cases in `test_4sum.py` guard:

- arrays shorter than four elements, and exactly four that do and do not sum to
  the target;
- the dedup requirement from several angles — `[2,2,2,2,2]`, `[0,0,0,0,0]`,
  `[0,0,0,0,1,1,1,1]`, `[1,1,1,1,2,2,2,2]`;
- `[1,-2,-5,-4,-3,3,3,5]` with target `-11`, where the answer is three negatives
  and the array holds a duplicate that is not part of it — this is the case that
  catches a prune skipping a valid pin when everything is negative;
- the constraint's `±10^9` extremes, where four values sum well outside 32-bit
  range;
- three 200-element arrays: no answer at all, the answer at the very start
  (`target = 10`) and at the very end (`target = 794`).

Answers are compared through `NORMALIZE`, since the order of the quadruplets
and the order inside one are both free.

## Notes

- **The two submissions measured here were the same program.** Both classes
  were byte-identical — the "list" version also built a `set` and returned
  `list(results)` — so the repo benchmark comparing them at 170.6 µs against
  177.2 µs was measuring one implementation against a copy of itself, and the
  1.04x was noise. The list version has since been written as intended.
- **With them genuinely different, the gap is still nothing.** On 200 elements:
  43.7 ms (set) against 44.3 ms (list) when the answer is empty, 1.38 ms against
  1.24 ms when it holds 1938 quadruplets. The set costs a hash per answer and
  buys no correctness, so the list is the better default — but not by enough to
  explain 8 ms against 20 ms on the judge. Those were two submissions at
  different times, and LeetCode's timing varies by more than this between runs
  of identical code.
- The lesson from the first point is cheaper than the benchmark: **diff two
  implementations before timing them.** A benchmark cannot tell you that its
  two inputs are the same program.
- What actually keeps a cubic scan practical is the pruning, not the collection.
  On a 200-element array with values in ±20, only 20% of the pinned pairs
  survive both tests; on 200 zeros, 0.5% do. On wide-range values, where the
  answer is empty, 98% survive — which is why that case costs 44 ms and the
  others cost under 2 ms.
- Pinning the *smallest* members is what makes local dedup sufficient, exactly
  as in [15. 3Sum](https://leetcode.com/problems/3sum/) — and the binary-search
  jump is the trick from
  [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/),
  which pays here for the same reason: it crosses runs of equal values in one
  move.
