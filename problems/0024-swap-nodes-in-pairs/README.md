---
number: 24
title: Swap Nodes in Pairs
difficulty: medium
topics: linked-list, recursion
url: https://leetcode.com/problems/swap-nodes-in-pairs/
status: solved
---

# 24. Swap Nodes in Pairs

## Problem

Given a linked list, swap every two adjacent nodes and return its head. You
must solve the problem without modifying the values in the list's nodes (i.e.,
only nodes themselves may be changed.)

**Example 1:**

```
Input: head = [1,2,3,4]

Output: [2,1,4,3]

Explanation:
```

![Example 1: the list 1 -> 2 -> 3 -> 4 becomes 2 -> 1 -> 4 -> 3](https://assets.leetcode.com/uploads/2020/10/03/swap_ex1.jpg)

**Example 2:**

```
Input: head = []

Output: []
```

**Example 3:**

```
Input: head = [1]

Output: [1]
```

**Example 4:**

```
Input: head = [1,2,3]

Output: [2,1,3]
```

**Constraints:**

- The number of nodes in the list is in the range `[0, 100]`.
- `0 <= Node.val <= 100`

## Approaches

| # | Approach | Time | Space | LeetCode |
|---|----------|------|-------|----------|
| 1 | `SolutionRecursiveSwap` | O(n) | O(n) | 0 ms, 19.14 MB |

### SolutionRecursiveSwap

The whole problem is one rewiring. With `first` and `second` at the front of
the list: `second` becomes the new head, `first` follows it, and whatever the
recursion returns for the rest of the list is attached behind `first`. A list
of fewer than two nodes is already its own answer, which is the base case.

Only links move — no `val` is ever written. That is what the statement demands,
and it is invisible to a comparison of output values, which is why the test
module checks node identity separately.

- **Time:** O(n) — each node is rewired once
- **Space:** O(n) — one stack frame per pair; the recursion is not tail
  recursive, since the returned list still has to be attached behind `first`

Recursion depth is `n/2`, so 50 frames at the constraint's 100 nodes and
comfortably inside Python's limit. It overflows around 2000 nodes — irrelevant
to the judge, but worth knowing before reusing the shape on a longer list.

### The `holder` node

`holder` is a `ListNode` allocated purely to hold a reference to `second`
while the links are rewritten. A local variable does the same job:

```python
second = head.next
head.next = self.swapPairs(second.next)
second.next = head
return second
```

That is not a different algorithm — it is the same recursion without an object
per pair. Measured (swap only, list construction subtracted):

| | 100 nodes | 1000 nodes |
|---|---|---|
| as written, `holder` per level | 7.6 µs | 103.0 µs |
| local variable instead | 2.7 µs | 50.1 µs |
| iterative, one sentinel total | 3.2 µs | 32.8 µs |

**2.8x at 100 nodes**, and the allocation is the whole difference. The judge
reports 0 ms either way — at n ≤ 100 there is nothing for it to see — but the
memory percentile is the kind of place it would show.

The iterative version keeps a single sentinel for the whole list rather than
one per pair, which also drops the space bound to O(1). It is not written here
as a class yet.

## Edge cases

The cases in `test_swap_nodes_in_pairs.py` guard:

- the statement's four examples, including the empty list — legal here, since
  the constraints say `[0, 100]` nodes;
- `[1, 2]`, the minimal swap;
- **odd lengths** (`[1,2,3]`, `[0,0,100,100,50]`, 99 nodes) — the final node
  must be left alone rather than dropped or paired with `None`;
- `[7,7,7,7]`, where every value is equal, so a solution that does nothing at
  all still produces the right values;
- `[0, 100]`, the value range;
- 100 and 99 nodes, the size limit in both parities;
- **two node-identity cases**, described below.

### Checking what the statement actually forbids

"Without modifying the values in the list's nodes" cannot be tested by
comparing values: a solution that swaps `val` fields returns exactly the same
output as one that relinks nodes. The last two cases check identity instead:

```python
def validate(actual, head):
    return NORMALIZE(actual) == expected and actual is not head and actual.next is head
```

A correct solution returns the node that was *second*, with the original head
right behind it. A value-swapper returns the original head object and fails.
Confirmed in both directions: a value-swapping implementation passes all ten
value cases and fails exactly these two; a relinking one passes all twelve.

## Notes

- **The rule the problem is really testing is invisible to the output.** Nine
  of the twelve cases would pass a solution that cheats by swapping values. If
  a statement forbids a technique rather than a result, the test has to inspect
  something other than the result — here, object identity.
- **A recursive solution is not O(1) space**, however little it allocates per
  call. One frame per pair is O(n), and writing O(1) in the docstring was the
  original claim here. The stack is as real as the heap.
- Allocating a node to hold a reference costs 2.8x on this input. Python names
  already are references; reaching for a container to hold one is the habit
  worth noticing.
- Related: [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)
  and [25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/),
  which is this problem with the pair generalized to a window of `k`.
