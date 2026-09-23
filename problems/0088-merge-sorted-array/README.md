---
number: 88
title: Merge Sorted Array
difficulty: easy
topics: array, two-pointers, sorting
url: https://leetcode.com/problems/merge-sorted-array/
status: solved
---

# 88. Merge Sorted Array

## Problem

You are given two integer arrays `nums1` and `nums2`, sorted in
**non-decreasing order**, and two integers `m` and `n`, representing the number
of elements in `nums1` and `nums2` respectively.

**Merge** `nums1` and `nums2` into a single array sorted in
**non-decreasing order**.

The final sorted array should **not** be returned by the function, but instead
be *stored inside the array* `nums1`. To accommodate this, `nums1` has a length
of `m + n`, where the first `m` elements denote the elements that should be
merged, and the last `n` elements are set to `0` and should be ignored.
`nums2` has a length of `n`.

**Example 1:**

```
Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.
```

**Example 2:**

```
Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
Explanation: The arrays we are merging are [1] and [].
The result of the merge is [1].
```

**Example 3:**

```
Input: nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
Explanation: The arrays we are merging are [] and [1].
The result of the merge is [1].
Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.
```

**Constraints:**

- `nums1.length == m + n`
- `nums2.length == n`
- `0 <= m, n <= 200`
- `1 <= m + n <= 200`
- `-10^9 <= nums1[i], nums2[j] <= 10^9`

**Follow up:** Can you come up with an algorithm that runs in `O(m + n)` time?

## Approaches

The answer goes *into* `nums1`, and that is the whole difficulty: the space to
write into is the space still holding unread input. Every approach either
sidesteps that conflict or resolves it.

| # | Approach | Time | Space | LeetCode | Local, m=n=100 |
|---|----------|------|-------|----------|----------------|
| 1 | `SolutionConcatSort` | O((m+n) log(m+n)) | O(m+n) | 0 ms, 19.36 MB | 1.1–1.8 µs |
| 2 | `SolutionForwardInsert` | O(m·n) | O(m) | 0 ms, 19.36 MB | 5.8–32.8 µs |
| 3 | `SolutionBackwardTwoPointer` | O(m+n) | O(1) | 0 ms, 19.15 MB | 6.6–12.9 µs |

The judge's runtime column cannot separate them at `n ≤ 200`; its memory column
can, and ranks them the way the space bounds do — 19.15 MB at the 95.89th
percentile for the O(1) approach against 19.36 MB at the 40.19th.

### SolutionConcatSort

Copy `nums2` over the padding and sort the whole thing.

It throws away the precondition — both halves arrive sorted and this ignores
that — which is why its bound is the worst of the three. What rescues it is
that the work happens in C: Timsort detects the two existing runs and merges
them, so the log factor is never really paid on input shaped like this.

- **Time:** O((m+n) log(m+n)) — the bound; in practice two runs merged linearly
- **Space:** O(m+n) — the sort's workspace, worst case

### SolutionForwardInsert

Walk forward through `nums1` and insert each `nums2` value where it belongs.

The invariant is that `nums1[:filled]` is sorted and holds everything consumed
so far. Inserting in the middle shifts the rest one place right, and that shift
is the price of going forward: the free room sits at the *end* of `nums1`,
behind the cursor rather than in front of it.

- **Time:** O(m·n) — every insertion may shift the whole prefix
- **Space:** O(m) — the slice assignment copies the tail it shifts

`del nums1[m:]` drops the padding **in place** so the list can grow back by
insertion. Writing `nums1 = nums1[:m]` instead builds a copy and leaves the
caller's list untouched — the solution then computes the right answer and
stores it nowhere, which is precisely the mistake this problem is built to
punish.

### SolutionBackwardTwoPointer

The answer to the follow-up, and the only approach here that resolves the
overwrite rather than sidestepping it: fill **from the end**.

Compare the two largest unread values and write the winner into the last free
slot. The write cursor starts at `m + n - 1` while the read cursors start at
`m - 1` and `n - 1`, so the write position is always at or ahead of both — it
can never land on something still unread. That single invariant removes both
the shifting and the extra array.

The loop ends when `nums2` is exhausted. Anything still left in `nums1` is
already below everything written *and already in the right place*, so it needs
no move — which is why there is no second loop.

- **Time:** O(m+n) — one write per element, no element moved twice
- **Space:** O(1) — three indices

Measured against the other two (m = n = 100, µs):

| shape | ConcatSort | ForwardInsert | BackwardTwoPointer |
|---|---|---|---|
| nums2 all larger | 1.1 | 5.8 | 6.6 |
| nums2 all smaller | 1.3 | 32.8 | 11.2 |
| interleaved | 1.8 | 29.4 | 12.9 |

Worth noting that the optimal algorithm is not the fastest program here:
`SolutionConcatSort` wins every shape because its loop runs in C while the
other two interpret Python bytecode per element. The asymptotics only take over
at sizes the constraints forbid — but the memory percentile still reflects the
difference the runtime column hides.

## Edge cases

The cases in `test_merge_sorted_array.py` guard:

- the statement's three examples, including `m = 0` and `n = 0`;
- **`nums2` entirely below `nums1`** (`[4,5,6]` + `[1,2,3]`) — the shape that
  breaks a forward merge writing into `nums1`, and the worst case for the
  insertion approach;
- `nums2` entirely above, the mirror;
- all values equal, and one element on each side;
- **real zeros against padding zeros** (`[-1,0,0,0], m=2` and an all-zero
  input) — the padding is indistinguishable from legitimate data, so anything
  keying off the value `0` rather than the count `m` fails here;
- the `±10^9` value extremes;
- `m=200, n=0` and `m=0, n=200`, one side empty at the size limit;
- two 100/100 cases at the limit, interleaved and disjoint.

Every expectation is `after(nums1=...)`: the function returns `None`, so the
harness compares the argument it passed in after the call — exactly what the
judge checks.

## Notes

- **`nums1 = nums1[:m]` was the bug**, and it is worth remembering as a rule
  rather than an incident: `x = ...` rebinds a name, while `x[:] = ...`,
  `del x[...]`, `x.sort()` and `x.append(...)` mutate the object. A function
  that rebinds a parameter cannot communicate anything back to its caller. The
  symptom was confusing because the computed answer was correct — it was just
  stored in a list nobody else could see.
- **A second bug hid behind the first**: with `m = 0` the truncated list is
  empty and `nums1[cursor]` raises `IndexError`. That is the statement's own
  Example 3. Inside the loop the invariant `cursor ≤ filled - 1` holds, so the
  only unsafe moment was entry — the loop was sound, its precondition was not.
- **The slower algorithm is the faster program.** `SolutionConcatSort` is
  O((m+n) log(m+n)) and beats both hand-written loops on every shape, because
  `list.sort` runs in C. All three report 0 ms on the judge, which at n ≤ 200
  can distinguish none of them — the memory column is the only place the
  difference shows.
- **Direction is the whole design.** The overwrite that forces `ForwardInsert`
  to shift and `ConcatSort` to sort simply does not exist when the merge runs
  backwards. Reaching for a bigger container or more work is the reflex; asking
  which end has the free space is the fix.
- Related: [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)
  is the same merge without the overwrite problem — linked lists have no
  contiguous storage to run out of, so the forward walk is free there.
