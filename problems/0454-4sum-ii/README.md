---
number: 454
title: 4Sum II
difficulty: medium
topics: principal, array, hash-table
url: https://leetcode.com/problems/4sum-ii/
status: solved
---

# 454. 4Sum II

## Problem

Given four integer arrays `nums1`, `nums2`, `nums3`, and `nums4` all of length
`n`, return the number of tuples `(i, j, k, l)` such that:

- `0 <= i, j, k, l < n`
- `nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0`

**Example 1:**

```
Input: nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]
Output: 2
Explanation:
The two tuples are:
1. (0, 0, 0, 1) -> nums1[0] + nums2[0] + nums3[0] + nums4[1] = 1 + (-2) + (-1) + 2 = 0
2. (1, 1, 0, 0) -> nums1[1] + nums2[1] + nums3[0] + nums4[0] = 2 + (-1) + (-1) + 0 = 0
```

**Example 2:**

```
Input: nums1 = [0], nums2 = [0], nums3 = [0], nums4 = [0]
Output: 1
```

**Constraints:**

- `n == nums1.length == nums2.length == nums3.length == nums4.length`
- `1 <= n <= 200`
- `-2^28 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 2^28`

## Approaches

The key invariant is **meet in the middle**: the four arrays are independent,
so instead of iterating all four simultaneously (O(n⁴)) the problem splits into
two independent O(n²) halves. Build a frequency map of every pairwise sum
`a + b` from `nums1 × nums2`, then for every `(c, d)` from `nums3 × nums4`
look up `-(c + d)` in that map. Each hit contributes its stored count.

Seven of the eight do exactly that. The first does not split at all — it loops
over three arrays and looks the fourth value up — which is why it is the only
one that is not quadratic.

`n` is the array length, `u` the number of distinct values in one array; u ≤ n.

| # | Approach | Time | Space | LeetCode | Local (50 runs) |
|---|---|---|---|---|---|
| 1 | `SolutionTripleLoop` | O(n·u + u³) | O(u) | TLE (48/133) | 108.0 ms |
| 2 | `SolutionSplitPairCount` | O(u²·n) | O(u²) | 2495 ms | 30.8 ms |
| 3 | `SolutionSplitAllCount` | O(n² + u²) | O(u²) | 426 ms | 5.08 ms |
| 4 | `SolutionSplitGuardedCount` | O(n·u + u²) | O(u²) | 407 ms | 4.54 ms |
| 5 | `SolutionSplitSetCount` | O(n·u + u²) | O(u²) | 353 ms | 3.92 ms |
| 6 | `SolutionSplitPruned` | O(n·u + u²) | O(u²) | 363 ms | 4.18 ms |
| 7 | `SolutionSplitDirect` | O(n·u + u²) | O(u²) | 301 ms | 3.82 ms |
| 8 | `SolutionSplitCounter` | O(n + u²) | O(u²) | 214 ms | 2.63 ms |

`u` is the number of distinct values in an array; `u ≤ n`, `u = n` in the
worst case. Classes 2–5 pay O(n) per distinct value during the frequency-map
build step because they call `list.count()` inside a loop. Local numbers from
`uv run lc bench 454 -r 200` on the test cases in `test_4sum_ii.py`.

### SolutionTripleLoop

Triple loop over unique values of `nums1`, `nums2`, `nums3`; for each triple
checks whether its negation exists in `nums4`. The frequency maps for the four
arrays are built upfront, so each lookup is O(1) — but only after the fix
described below; as submitted the membership test rebuilt a set every time.

- **Time:** O(n·u + u³) — u³ triples, plus u calls to `list.count()`
- **Space:** O(u) — four frequency maps, each with at most u entries

As submitted, the innermost test read `if -a - b - c in set(nums4)`, which
rebuilt that set on every iteration: an O(n) "lookup" that made the whole thing
O(u³·n). Hoisting the four `set()` calls out of the loops — no other change,
same answers — is worth 12x at u=10 and 17x at u=40, and takes the 200-distinct
case from 21 s to 691 ms. It is still the slowest of the eight, because u³
against u² is the real problem.

### SolutionSplitPairCount

First step toward meet-in-the-middle: build `sums12` mapping every pairwise sum
`a + b` to its count, then build `sums34` likewise for `nums3 × nums4`, then
join the two maps. The loop structure is O(u²), but frequency counts are
computed with `list.count()` inside the pairing loops — once per unique pair
`(a, b)` rather than once per unique value — making the frequency build step
O(u² · n).

- **Time:** O(u² · n) — calling `list.count()` on `nums2` inside the nested loops
- **Space:** O(u²) — `sums12` and `sums34` hold at most u² entries each

### SolutionSplitAllCount

Same structure as `SolutionSplitPairCount`, but the four frequency maps are built
in a single loop before pairing. `list.count()` is still called once per
element index — n calls per array, each O(n) — so repeated values trigger
redundant scans.

- **Time:** O(n² + u²) — n calls to `list.count()`, then O(u²) pairing loops
- **Space:** O(u²) — as above

### SolutionSplitGuardedCount

Guards each `.count()` call with a membership check (`if n not in c`), so a
repeated element is counted only once. Correct for any input, but the
membership check does not change the asymptotic bound.

- **Time:** O(u² + n·u) — one `.count()` per unique value, each O(n)
- **Space:** O(u²) — as above

### SolutionSplitSetCount

Builds the four sets of unique values *before* entering the loops, then runs
one `.count()` per unique value rather than rediscovering uniqueness mid-loop.
This is the first genuinely clean expression of the build step, even though
`.count()` is still O(n) per call.

- **Time:** O(u² + n·u) — frequency build is O(n·u); pairwise join is O(u²)
- **Space:** O(u²) — as above

### SolutionSplitPruned

Same as `SolutionSplitSetCount` but builds `sums34` with a pruning step: a
`(c, d)` pair whose negated sum `-(c+d)` is absent from `sums12` cannot
contribute to the total, so it is skipped with `continue`. This avoids
populating `sums34` with entries the final join would ignore anyway.

- **Time:** O(n·u + u²) — the prune removes entries that would contribute 0,
  but the frequency build still costs u calls to `list.count()`
- **Space:** O(u²)

### SolutionSplitDirect

Skips building `sums34` entirely. For each unique `(c, d)` pair, look up
`-(c+d)` in `sums12` and accumulate directly into the total. One fewer dict
allocation and one fewer pass over the data compared to `SolutionSplitPruned`.

- **Time:** O(n·u + u²) — one hash lookup per unique pair, no third pass; the
  frequency build is unchanged from above
- **Space:** O(u²) — only `sums12` is retained

### SolutionSplitCounter

Uses `Counter` from `collections` instead of manual frequency maps. `Counter`
is a `dict` subclass that counts automatically, removing the separate
`.count()` or iteration step and making the intent clear. Measured at 214 ms on
LeetCode (99.65th percentile).

- **Time:** O(n²) — `Counter(nums)` is O(n); building `sums12` is O(n²)
- **Space:** O(n²) — `sums12` holds at most n² entries

See [`explain.ipynb`](explain.ipynb) for traced execution on a small input and
a measured comparison of the approaches.

## Edge cases

The cases in `test_4sum_ii.py` guard:

- the minimal n = 1 case where all arrays are `[0]` — output is 1, not 0;
- the two-element example from the problem statement;

## Notes

- **Meet in the middle** is the general technique: whenever a problem asks
  about *k* independent groups, split into k/2 + k/2, enumerate each half, and
  join. Here k = 4 drops O(n⁴) to O(n²). The same idea appears in
  [1. Two Sum](https://leetcode.com/problems/two-sum/) (k = 2, one half is a
  scan, the other is a hash-map lookup) and generalises to exponential search
  over subsets.
- The progression from `SolutionSplitPairCount` to `SolutionSplitDirect` shows
  that the O(n·u) frequency-build cost comes from calling `list.count()` (an
  O(n) scan) inside a loop. Switching to `Counter` or to a single-pass
  eliminates it.
- **`Counter` vs manual dict**: both are O(n) for frequency building; `Counter`
  wins on clarity and avoids the `setdefault`/`get` boilerplate, at no cost.
- **The benchmark tells the real story.** `SolutionSplitPairCount` to
  `SolutionSplitAllCount` is a 13.0x→2.0x drop, not because the algorithm
  changed but because `SolutionSplitPairCount` calls `list.count()` once per
  unique *pair* (u²·n calls), while `SolutionSplitAllCount` onward call it once
  per unique *value* (n·u calls). On the test inputs (n = 100–155), `n` and
  `u` are nearly equal, so that single refactor is worth 6.5x. The remaining
  2x from there to `SolutionSplitCounter` comes from eliminating `.count()`
  entirely with `Counter`.
