"""Cases for 653. Two Sum IV - Input is a BST.

Trees are written the way LeetCode writes them — level order, ``None`` for a
missing child — and ``tree()`` turns that list into nodes. ``bst()`` builds a
height-balanced tree from sorted values, for the cases too large to spell out.
"""

from collections import deque

from lc.harness import check, load_solutions

SOLUTIONS = load_solutions(__file__)


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"tree({level_order(self)})"


def tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    pending = iter(values[1:])
    for value in pending:
        node = queue.popleft()
        if value is not None:
            node.left = TreeNode(value)
            queue.append(node.left)
        right = next(pending, None)
        if right is not None:
            node.right = TreeNode(right)
            queue.append(node.right)
    return root


def bst(values):
    if not values:
        return None
    middle = len(values) // 2
    return TreeNode(values[middle], bst(values[:middle]), bst(values[middle + 1 :]))


def level_order(root):
    values = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while values and values[-1] is None:
        values.pop()
    return values


EXAMPLE = [5, 3, 6, 2, 4, None, 7]
BALANCED = list(range(1, 1024))

CASES = [
    ((tree(EXAMPLE), 9), True),
    ((tree(EXAMPLE), 28), False),
    ((tree(EXAMPLE), 5), True),
    ((tree(EXAMPLE), 10), True),
    ((tree(EXAMPLE), 14), False),
    ((tree([1]), 2), False),
    ((tree([2, 1, 3]), 4), True),
    ((tree([2, 1, 3]), 6), False),
    ((tree([1, None, 2]), 3), True),
    ((tree([0, -2, 3]), 1), True),
    ((tree([-10000, None, 10000]), 0), True),
    ((bst(BALANCED), 1024), True),
    ((bst(BALANCED), 20000), False),
]


def test_solution(solution, case, equal):
    check(solution, case, equal)
