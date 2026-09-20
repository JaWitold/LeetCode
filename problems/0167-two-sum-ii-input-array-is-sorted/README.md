---
number: 167
title: Two Sum II - Input Array Is Sorted
difficulty: medium
topics: array, two-pointers, binary-search
url: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
status: solved
---

# 167. Two Sum II - Input Array Is Sorted

## Problem

You are given a **1-indexed** array of integers `numbers` that is already **sorted in non-decreasing order**.

Find **two** numbers such that they add up to a specific `target` number. Let these two numbers be `numbers[index_1]` and `numbers[index_2]` where `1 <= index1 < index2 <= numbers.length`.

Return the indices of the two numbers `index_1` and `index_2` as an integer array `[index_1, index_2]` of length 2.

The tests are generated such that there is **exactly one solution**. You **may not** use the same element twice.

Your solution must use only constant extra space.

**Example 1**:

```
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
```

**Example 2**:

```
Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
```
**Example 3**:

```
Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].
``` 

**Constraints**:

- `2 <= numbers.length <= 3 * 10^4`
- `-1000 <= numbers[i] <= 1000`
- `numbers is sorted in non-decreasing order.`
- `-1000 <= target <= 1000`
- The tests are generated such that there is exactly one solution.

## Approaches

Every approach here is a variation on one idea: with the array sorted, a pair
that is too small can only be fixed by taking a larger left value, and a pair
that is too large only by taking a smaller right one. What separates them is
how far a pointer moves per step, and that only matters because the values are
capped at ±1000 — an array of 30 000 entries holds at most 2001 distinct
values, so it is mostly runs of duplicates. Crossing a run in one move is the
whole game.

| # | Approach | Time | Space | LeetCode |
|---|----------|------|-------|----------|
| 1 | `SolutionHashMap` | O(n) | O(n) | 7 ms |
| 2 | `SolutionTwoPointers` | O(n) | O(1) | 7 ms |
| 3 | `SolutionTwoPointersSkipImpossible` | O(n) | O(1) | 9 ms |
| 4 | `SolutionTwoPointersSkipDuplicates` | O(n) | O(1) | 7 ms |
| 5 | `SolutionBisectJump` | O(d log n) | O(1) | — |
| 6 | `SolutionMidpointProbe` | O(n) | O(1) | 3 ms |
| 7 | `SolutionBisectRunEnd` | O(d log n) | O(1) | 0 ms |
| 8 | `SolutionInlineBisectJump` | O(d log n) | O(1) | 0 ms |

`d` is the number of distinct values met, at most 2001 under the constraints.

### SolutionHashMap

Two Sum's answer, carried over unchanged: remember the complement each element
is waiting for. Correct, and it ignores the sorted input entirely — which also
means it is the one approach that breaks the problem's "constant extra space"
requirement. LeetCode accepts it anyway.

- **Time:** O(n) — one pass, look-up and insert amortized O(1)
- **Space:** O(n) — one map entry per element seen

### SolutionTwoPointers

The textbook walk inwards. If the sum is short of the target, every partner for
the current left value lies at or left of the current right index, so that
value can be discarded — and symmetrically on the other side. One element is
eliminated per step.

- **Time:** O(n) — each step discards one candidate
- **Space:** O(1) — two indices

### SolutionTwoPointersSkipImpossible

The same walk, except the inner loops run past every index that cannot pair
with the opposite end. The pointers still only move inwards, so the total work
is unchanged; what changes is that a whole run is crossed inside one outer
iteration instead of one per iteration. That is why it is the quickest of the
linear walkers in local measurements despite the 9 ms on the judge.

- **Time:** O(n) — pointers are monotone, so the inner loops are amortized
- **Space:** O(1) — two indices

### SolutionTwoPointersSkipDuplicates

Same reasoning narrowed to equal values: once a value is rejected against the
other end, every copy of it is rejected too. Cheaper per element than the plain
walk, but it still touches every element of a run.

- **Time:** O(n) — a run costs one comparison per element
- **Space:** O(1) — two indices

### SolutionBisectJump

Instead of walking, binary-search the first index whose value could reach the
target with the opposite end, and jump there. Each outer iteration then
consumes at least one distinct value, and the constraints cap those at 2001
however long the array is.

- **Time:** O(d log n) — d distinct values, each a binary search
- **Space:** O(1) — `bisect` searches in place

It survives every shape measured: 0.029 ms on a 30 000-long wall of duplicates
and 0.003 ms on 2001 distinct values, because the jump is driven by the target
rather than by run boundaries.

### SolutionMidpointProbe

A hand-rolled halving. If the midpoint holds the same value as the pointer, the
whole span up to it is that value and can be skipped; otherwise take one step.
One probe does not find the end of a run, so crossing a long run takes several
iterations — but each is a halving, so it is still fast in practice.

- **Time:** O(n) worst case — a single probe can fail to skip anything
- **Space:** O(1) — two indices and a midpoint

### SolutionBisectRunEnd

Binary-search the end of the run of equal values, written out by hand because
the predicate is "still equal to this value" rather than an ordering
comparison. Each move lands one past every copy of the value just rejected, so
one outer iteration consumes one distinct value.

- **Time:** O(d log n) — d distinct values, each found by binary search
- **Space:** O(1) — two indices, the searches are iterative

0 ms and 100% on the judge, because its tests are duplicate-heavy and d is
tiny there. The cost shows on the other shape: with all values distinct every
run has length one, so each binary search pays O(log n) to advance a single
index. On 2001 distinct values it measures **1.43 ms against 0.14 ms for the
plain walk** — ten times slower than the approach it improves on. The value
constraint is what keeps that case off the judge.

### SolutionInlineBisectJump

The same jump as `SolutionBisectJump`, with the binary searches written out
inline: no function call, no slice bookkeeping per step. Matches it on every
shape measured and keeps the judge's 0 ms.

- **Time:** O(d log n) — d distinct values, each a binary search
- **Space:** O(1) — four indices

The searches look off by one on purpose. Closing with `probe - 1` and
`probe + 1` on both sides means the landing index can stop *short* of the true
boundary but never past it: `lo` only advances from a probe strictly below the
needed value, so the answer cannot be skipped. A conservative landing costs an
extra outer iteration, never a wrong result — which is what makes this the one
hand-rolled search here that is safe to trust.

## Edge cases

The cases in `test_two_sum_ii_input_array_is_sorted.py` guard:

- the pair being a repeated value (`[3, 3]`) and repeats that are *not* the
  answer (`[1, 1, 1, 2, 7]`) — an index paired with itself, or a duplicate skip
  that skips too far;
- negatives either side of zero, and answers pinned to the first two, the last
  two, and both far ends — 1-indexing and off-by-one errors that happen to look
  right on two-element inputs;
- `[-1] * 2998 + [1, 1]` with target 2, the shape of LeetCode's failing test at
  a size that keeps the suite under a second. No approach kept here is
  quadratic any more, so it now guards against a future one that scans;
- `[-1, -1] + [1, 1] * 2998`, which has ~18M valid answers, so it asserts
  through a validator instead of a fixed pair. Approaches legitimately disagree
  here: the hash map answers `[3, 4]`, a two-pointer walk `[3, 5998]`.

Deliberately **not** in `CASES`: the full 30 000-element version of the TLE
case, which would add 25 s to every test run to make a point already made at
n=3000.

## Notes

- A TLE is not always slowness. One discarded attempt — the midpoint probe
  wrapped in an inner loop — came back "Time Limit Exceeded,
  21/26" and was rewritten twice as if it needed optimizing. It was an infinite
  loop: its inner guard read `midpoint >= right`, but the midpoint is never to
  the right of `right`, so on a wide window nothing moved and the outer loop
  repeated forever. `[-2, -2, -1, -1, -1]` with target `-4` is the smallest
  case; an exhaustive sweep of sorted arrays of length ≤ 6 hangs on 116 of 1389
  legal inputs and answers none of them wrongly. It is not kept in
  `solutions.py` — a non-terminating class would hang the suite rather than
  fail it — but `explain.ipynb` reproduces it inline. Treat a TLE on an
  algorithm that should already be fast enough as a suspected infinite loop.
- The constraints are the algorithm. Values capped at ±1000 with arrays up to
  30 000 entries means duplicates are unavoidable, which is what makes run
  skipping pay and what hides the weakness of `SolutionBisectRunEnd`. Reading
  the constraint block first is worth more here than any micro-optimization.
- LeetCode's percentile is noisy and its "Memory beats 9%" figure was identical
  for eight very different approaches — only the millisecond column carried
  information, and even that came from one fixed test distribution.
- Related: [1. Two Sum](https://leetcode.com/problems/two-sum/) (unsorted, so
  the hash map is the answer rather than a leftover) and
  [15. 3Sum](https://leetcode.com/problems/3sum/), which is this two-pointer
  walk nested inside a loop, duplicate skipping included.
