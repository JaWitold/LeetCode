---
number: 19
title: Remove Nth Node From End of List
difficulty: medium
topics: linked-list, two-pointers
url: https://leetcode.com/problems/remove-nth-node-from-end-of-list/
status: solved
---

# 19. Remove Nth Node From End of List

## Problem

Given the `head` of a linked list, remove the `n`^th node from the end of the list and return its `head`.

**Example 1:**

```
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
```

**Example 2:**

```
Input: head = [1], n = 1
Output: []
```

**Example 3:**

```
Input: head = [1,2], n = 1
Output: [1]
```

**Constraints:**

- The number of nodes in the list is `sz`.
- `1 <= sz <= 30`
- `0 <= Node.val <= 100`
- `1 <= n <= sz`

**Follow up:** Could you do this in one pass?

## Approaches

| # | Approach | Time | Space | LeetCode | Local (500 runs) |
|---|---|---|---|---|---|
| 1 | `SolutionTwoPointers` | O(sz) | O(1) | 0 ms (100.00%, 19.23 MB) | 244.0 µs |

### SolutionTwoPointers

Advance a fast pointer `fast` by `n` steps from `head`, creating an $n$-step lead
over `slow`. Then advance both `fast` and `slow` in lockstep while tracking
`slow`'s predecessor `prev`. When `fast` reaches `None`, `slow` is sitting
on the target node to delete and `prev` is its predecessor.

Because no dummy node precedes `head`, if `prev is None` after the walk, the
node to remove is the head itself (so `head = slow.next`). Otherwise,
`prev.next` is re-pointed to bypass `slow`.

- **Time:** O(sz) — single pass over the list ($sz$ node steps total)
- **Space:** O(1) — three pointers (`slow`, `fast`, `prev`)

See [`explain.ipynb`](explain.ipynb) for a step-by-step trace of the pointer
positions and edge-case branching.

## Edge cases

The cases in `test_remove_nth_node_from_end_of_list.py` guard:

- **Removing the head** (`n == sz`): list of 2 nodes (`n = 2`) and list of 4
  nodes (`n = 4`), where `prev` remains `None` and `head` must become
  `slow.next`.
- **Single-node list** (`sz = 1, n = 1`): where the list becomes empty (`None`).
- **Removing the tail** (`n = 1`): list of 2 nodes (`n = 1`) and 4 nodes
  (`n = 1`), setting the predecessor's `next` to `None`.
- **Removing an interior node**: Example 1 (`[1, 2, 3, 4, 5], n = 2`) and 3-node
  list (`[1, 2, 3], n = 2`).
- **Maximum constraint size** ($sz = 30$): removing head (`n = 30`), middle
  (`n = 15`), and tail (`n = 1`).

## Notes

- **Two-pointer delayed window**: Moving `fast` $n$ steps ahead allows
  locating the $n$-th node from the end in a single pass without knowing the total
  length of the list upfront.
- **Handling the head without a dummy node**: When deleting in a singly linked
  list, one needs the predecessor. Since the head has no predecessor, `prev`
  remains `None`, requiring an explicit branch to reassign `head = slow.next`.
- Measured at **0 ms** (100.00th percentile) and **19.23 MB** (65.93th percentile) on LeetCode.
