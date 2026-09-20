---
number: 653
title: Two Sum IV - Input is a BST
difficulty: easy
topics: mid-level, hash-table, two-pointers, tree, depth-first-search, breadth-first-search, binary-search-tree, binary-tree
url: https://leetcode.com/problems/two-sum-iv-input-is-a-bst/
status: todo
---

# 653. Two Sum IV - Input is a BST

## Problem

Given the `root` of a binary search tree and an integer `k`, return `true` if
there exist two elements in the BST such that their sum is equal to `k`, or
`false` otherwise.

**Example 1:**

```
Input: root = [5,3,6,2,4,null,7], k = 9
Output: true
```

**Example 2:**

```
Input: root = [5,3,6,2,4,null,7], k = 28
Output: false
```

**Constraints:**

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-10^4 <= Node.val <= 10^4`
- `root` is guaranteed to be a valid binary search tree.
- `-10^5 <= k <= 10^5`

## Approaches

Five of the six are [1. Two Sum](https://leetcode.com/problems/two-sum/)'s
complement trick poured over a tree walk: visit every node and ask whether an
earlier node is waiting for this value. They differ only in *what remembers the
complements* and *in what order the walk visits nodes* — and those two axes
account for the entire 27 ms → 0 ms spread. The sixth ignores the trick and
uses the ordering the problem actually gives.

| # | Approach | Time | Space | LeetCode |
|---|----------|------|-------|----------|
| 1 | `SolutionRecursiveList` | O(n²) | O(n) | 27 ms |
| 2 | `SolutionStackSet` | O(n) | O(n) | 8 ms |
| 3 | `SolutionRecursiveSetSeeded` | O(n) | O(n) | 3 ms |
| 4 | `SolutionRecursiveSet` | O(n) | O(n) | 3 ms |
| 5 | `SolutionSearchPerNode` | O(n·h) | O(h) | 8 ms |
| 6 | `SolutionQueueSet` | O(n) | O(n) | 0 ms |

`h` is the tree height: `log n` when balanced, `n` when the BST is a chain.

### SolutionRecursiveList

The complement trick with the complements kept in a list. Worth keeping
precisely because it is `SolutionRecursiveSetSeeded` with one word changed, so
the distance between them is purely the cost of `in`.

- **Time:** O(n²) — `in` on a list is a scan, once per node
- **Space:** O(n) — one complement per node, plus O(h) recursion

### SolutionStackSet

The same trick, depth-first over an explicit stack. Children are pushed
unconditionally and `None` is filtered on the way back out, which costs an
extra push and pop for every missing child — in a balanced tree that is roughly
one wasted round trip per node.

- **Time:** O(n) — one set look-up per node
- **Space:** O(n) — the set, plus O(h) of stack

### SolutionRecursiveSetSeeded

The list swapped for a set. The root is handled by seeding its complement
before the walk starts, so the recursion begins at the children.

- **Time:** O(n) — amortized O(1) membership
- **Space:** O(n) — the set, plus O(h) recursion

### SolutionRecursiveSet

The same walk without the seeding, recursing from the root. Nothing is gained
or lost — it is the tidier way to write the same thing, and measures the same.

- **Time:** O(n) — as above
- **Space:** O(n) — as above

### SolutionSearchPerNode

The only approach that uses the BST ordering: for each node, descend the tree
looking for `k - node.val`, rejecting the node that finds itself. No set at
all, which is what makes its memory the lowest of the six.

- **Time:** O(n·h) — a descent per node; O(n log n) balanced, O(n²) on a chain
- **Space:** O(h) — the traversal stack, and no complement set

It is the fastest of all six when a pair exists and is found early, because the
very first node checked may locate its partner — and the slowest of the O(n)
family when no pair exists, since every node pays a full descent.

### SolutionQueueSet

The complement trick breadth-first, iterating the queue as it grows:
`for node in queue` walks a list that is still being appended to, so there is
no `pop` and no `deque`. Children are checked before being appended, so no
`None` ever enters the queue.

- **Time:** O(n) — one set look-up per node
- **Space:** O(n) — the set, plus up to O(n) of queue at the widest level

## Edge cases

The cases in `test_two_sum_iv_input_is_a_bst.py` guard:

- `k` equal to twice a node's value (`14` on the example tree, `6` on
  `[2,1,3]`, `2` on `[1]`) — an element paired with itself, which is the
  mistake the complement trick invites;
- the pair spanning the root's two subtrees (`9`, `10`) as well as sitting
  inside one (`5`) — a walk that forgets nodes across subtrees passes the first
  and fails the second;
- a single node, a missing child (`[1,null,2]`), negatives across zero, and the
  value extremes `±10000`;
- a 1023-node balanced BST both with a pair and without one. The no-pair case is
  the only one that forces every approach to visit every node.

Trees are written the way LeetCode writes them — level order with `null`
holes — and built by `tree()` in the test module; `bst()` builds the balanced
one from sorted values.

## Notes

- **A set instead of a list is the single biggest win here**, and it is not a
  micro-optimization: it changes the complexity from O(n²) to O(n). Measured on
  a 8191-node tree with no pair, 177 ms against 1.37 ms. The two
  implementations differ by one word.
- **The queue-versus-stack gap has nothing to do with the queue.** Those two
  implementations differ in three ways at once, so comparing them measures
  nothing in particular. Changing one thing at a time on an 8191-node tree with
  no pair (min of 15 runs, so the ordering is stable):

  | variant | ms |
  |---|---|
  | `SolutionStackSet` — depth-first, pushes `None`, `pop` | 1.10 |
  | control: depth-first, no `None`, `pop` | 0.91 |
  | control: breadth-first, no `None`, `deque.popleft` | 0.90 |
  | `SolutionQueueSet` — breadth-first, no `None`, `for node in queue` | 0.74 |

  Not pushing children that do not exist buys 0.19 ms and iterating the growing
  list instead of popping buys 0.16 ms; switching depth-first to breadth-first
  buys **0.01 ms**, which is nothing. The first measurement of this looked like
  the opposite until it was repeated — single runs here vary by more than the
  effect being measured.
- **Where the order genuinely matters is when a pair exists.** Depth-first
  plunges down one side before it can see the other, while breadth-first has
  both subtrees in hand after two levels — and in a BST, a pair summing to a
  mid-range `k` usually straddles the root. That is why `SolutionQueueSet` and
  `SolutionSearchPerNode` return instantly on such inputs while the depth-first
  walks take half a millisecond. That is where breadth-first earns its keep —
  not on the full walk.
- Not tried here, and the approach most reviewers would ask for: in-order
  traversal into a sorted list, then the
  [167. Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
  two-pointer walk. Same O(n) time, and the pointers make the O(h) space claim
  honest.
