---
number: 21
title: Merge Two Sorted Lists
difficulty: easy
topics: linked-list, recursion
url: https://leetcode.com/problems/merge-two-sorted-lists/
status: solved
---

# 21. Merge Two Sorted Lists

## Problem

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one **sorted** list. The list should be made by
splicing together the nodes of the first two lists.

Return the head of the merged linked list.

**Example 1:**

```
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```

**Example 2:**

```
Input: list1 = [], list2 = []
Output: []
```

**Example 3:**

```
Input: list1 = [], list2 = [0]
Output: [0]
```

**Constraints:**

- The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in **non-decreasing order**.

## Approaches

| # | Approach | Time | Space | LeetCode |
|---|----------|------|-------|----------|
| 1 | `SolutionSpliceWithSentinel` | O(n + m) | O(1) | 0 ms |

### SolutionSpliceWithSentinel

Walk both lists at once, always attaching whichever head is smaller, and stop
as soon as one runs out.

The invariant: `tail` is the last node of the merged list, and everything still
reachable from `list1` and `list2` is greater than or equal to it. Taking the
smaller head keeps that true. Because both inputs are sorted, whichever list
survives the loop is *already* in order and correctly placed after everything
merged so far — so the remainder is attached in a single step rather than
walked, and that one line replaces the loop most first attempts write.

Two details carry it:

- **The sentinel.** Without a dummy node, the first link needs a special case
  (which list did the head come from?) and every later link needs a null check.
  With one, the answer is simply whatever ended up after it.
- **`<=` rather than `<`.** On a tie the node comes from `list1`, which makes
  the merge stable. Verified: merging `1ᴬ → 3ᴬ` with `1ᴮ → 4ᴮ` yields
  `1ᴬ, 1ᴮ, 3ᴬ, 4ᴮ`.

No node is allocated per element — the input nodes are relinked, which is what
"splicing together the nodes of the first two lists" asks for.

- **Time:** O(n + m) — each node is visited once and linked once
- **Space:** O(1) — one sentinel and one cursor, whatever the input size

## Edge cases

The cases in `test_merge_two_sorted_lists.py` guard:

- both lists empty, and each side empty in turn — the constraints allow
  `[0, 50]` nodes, so empty input is legal here and `tail.next = ...` must
  cope with both operands being `None`;
- equal values across and within lists (`[1]` with `[1]`, `[1,1,1]` with
  `[1,1]`), which is where a `<` comparison would still be correct but unstable;
- the `±100` value extremes;
- fully disjoint ranges in **both** orders, so the answer is entirely one list
  followed by the other — the shape that catches a dropped remainder;
- very uneven lengths (`[2]` against `[1,3,5,7,9]`);
- two 50-node lists at the constraint limit, interleaved and disjoint.

`NORMALIZE` converts whatever a solution returns — a node chain or `None` —
back to bracket notation, so a failure prints two lists instead of two object
addresses.

## Notes

- **The first attempt returned `[]` for every input.** It advanced the cursor
  with `current = list1` instead of linking with `current.next = list1`, so
  `sentinel.next` was never assigned and the picked nodes were dropped. The
  lesson is that a cursor walk over a list you are *building* needs two
  statements — link, then advance — where a walk over a list you are *reading*
  needs one.
- **It also had two unreachable branches.** `if list1 is None` inside a
  `while list1 is not None and list2 is not None` loop can never fire; the
  exhausted-list handling has to come *after* the loop. Dead code that looks
  like it handles a case is worse than no code, because it reads as covered.
- The disjoint-range cases are what would have caught the second bug on its
  own: a merge that drops the remainder still passes every case where the two
  lists interleave to the end.
- Related: this is the merge step of merge sort, and
  [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)
  is this routine applied pairwise or through a heap.
