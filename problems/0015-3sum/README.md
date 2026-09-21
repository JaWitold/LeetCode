---
number: 15
title: 3Sum
difficulty: medium
topics: array, two-pointers-sorting
url: https://leetcode.com/problems/3sum/
status: solved
---

# 15. 3Sum

## Problem

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

 

Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.
Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.
Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.
 

Constraints:

3 <= nums.length <= 3000
-105 <= nums[i] <= 105

## Approaches

All three sort first, then fix one element and two-pointer the rest. What
separates them is *which* element gets fixed — which decides whether duplicate
triplets are avoidable at all — and how far a pointer moves per step.

| # | Approach | Time | Space | LeetCode |
|---|----------|------|-------|----------|
| 1 | `SolutionMiddlePivotSet` | O(n²) | O(t) | 1474 ms |
| 2 | `SolutionTwoPointersPruned` | O(n²) | O(1) | 408 ms |
| 3 | `SolutionBisectJump` | O(n² log n) | O(1) | 327 ms |

`t` is the number of triplets in the answer, which can itself be O(n²). Space
excludes the output and the sort's own workspace.

### SolutionMiddlePivotSet

Fix the **middle** element and close in from both ends of the whole array.

That choice is what forces the set. With the middle element pinned, the same
triplet is reachable from more than one pivot, so duplicates arise during the
scan rather than only from repeated values — and no amount of skipping equal
neighbours removes them. A set of tuples absorbs them afterwards.

- **Time:** O(n²) — a full two-pointer sweep for each of n pivots
- **Space:** O(t) — one entry per distinct triplet found

### SolutionTwoPointersPruned

Fix the **smallest** element, then two-pointer the suffix to its right.

Fixing the first element is what removes the set: each triplet is produced only
by the pivot that is its smallest member, so skipping equal values on all three
positions is enough to keep the answer unique. That is the whole difference
between 1474 ms and 408 ms, and it is a correctness argument, not a tuning one.

Three prunes ride on the sort: a positive first value ends the search (nothing
after it can reach zero), a first value whose two smallest partners already
overshoot ends it too, and one whose two largest partners still fall short is
skipped.

- **Time:** O(n²) — one suffix sweep per distinct first value
- **Space:** O(1) — three indices; the output is not counted

### SolutionBisectJump

The same walk, with each pointer binary-searching the first index that could
complete the triplet instead of stepping one at a time — the trick from
[167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/),
reused inside the inner loop.

- **Time:** O(n² log n) worst case — each inner step is a binary search that
  advances at least one index
- **Space:** O(1) — as above

The worst-case bound is *worse* than approach 2, and measurement is what
decides between them:

| input (n = 3000) | `TwoPointersPruned` | `BisectJump` |
|---|---|---|
| wide value range, few duplicates | 247 ms | 246 ms |
| values in ±30, heavy duplication | 4.3 ms | 2.8 ms |
| all zeros | 0.4 ms | 0.4 ms |

With values spread out, a jump lands one index along and pays O(log n) for what
a step did for free — the two break even. The gain comes entirely from runs of
equal values, where one jump crosses the whole run, and the LeetCode figures
(408 ms against 327 ms) say its tests contain plenty of those.

## Edge cases

The cases in `test_3sum.py` guard:

- the dedup requirement from several angles — `[0,0,0,0]` and `[0]*30` (one
  triplet, not one per combination), `[-1,-1,-1,2,2,2]`, `[-2,0,1,1,2]`, and
  `[-4,-2,-2,0,2,2,4]` with four overlapping triplets;
- inputs with no answer at all: `[1,2,3]`, `[-1,-2,-3]`, and 300-element
  ascending and descending runs that force the full scan;
- the constraint's value extremes, `±100000`;
- a sparse array of powers of two with exactly one triplet, which an
  over-eager skip loses.

Answers are compared through `NORMALIZE`, since both the order of the triplets
and the order within a triplet are free.

## Notes

- **Which element you fix is a correctness decision, not a style one.** Pinning
  the middle element makes duplicate triplets unavoidable during the scan, so a
  set has to clean up afterwards; pinning the smallest makes each triplet
  reachable exactly once, and skipping equal values suffices. Approach 1 is 3.6x
  slower on the judge for that reason alone.
- **A dedup skip compares against where the pointer came from, not where it is
  going.** The first version of approach 3 read `nums[left] == nums[left + 1]`
  after `left += 1`, which skips a value that was never reported and misses
  triplets. It failed only the duplicate-heavy cases — 167 of 4000 random
  arrays — and was invisible on the examples. Approach 2, written the same day,
  had it right: `nums[left - 1]`.
- Binary search is not automatically an upgrade. It costs O(log n) to make a
  move that a step makes in O(1), so it only pays when the move is long —
  duplicates here, and the same story as in
  [167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/).
- `nums.sort()` mutates the caller's list. The harness deep-copies arguments per
  run so cases cannot be corrupted between approaches, but on the judge it is
  worth knowing that the input is not left intact.
