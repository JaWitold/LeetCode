"""653. Two Sum IV - Input is a BST — https://leetcode.com/problems/two-sum-iv-input-is-a-bst/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.

Five of the six are the Two Sum complement trick applied to a traversal: walk
the tree, and for every node ask whether some earlier node is waiting for this
value. They differ in what remembers the complements and in what order the
walk visits nodes. The sixth ignores the trick and uses the BST ordering.
"""

from typing import Optional

ENTRY = "findTarget"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class SolutionRecursiveList:
    """Complement trick with the complements kept in a list.

    Correct, and the reason to keep it: it is the same algorithm as
    :class:`SolutionRecursiveSetSeeded` with one word changed, so the gap
    between them is purely the cost of ``in`` on a list against a set.

    O(n^2) time, O(n) space.
    """

    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        seen = [k - root.val]

        def search(node: Optional[TreeNode]) -> bool:
            if node is None:
                return False

            if node.val in seen:
                return True
            seen.append(k - node.val)
            return search(node.left) or search(node.right)

        return search(root.left) or search(root.right)


class SolutionStackSet:
    """Complement trick over an explicit stack, so depth-first without recursion.

    Children are pushed unconditionally and ``None`` is filtered on the way out,
    which costs an extra push and pop per leaf.

    O(n) time, O(n) space.
    """

    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        stack = [root]
        seen = set()

        while stack:
            node = stack.pop()

            if node is None:
                continue
            if node.val in seen:
                return True

            seen.add(k - node.val)

            stack.append(node.left)
            stack.append(node.right)
        return False


class SolutionRecursiveSetSeeded:
    """:class:`SolutionRecursiveList` with a set, which is the whole difference.

    The root is handled by seeding its complement before the walk starts, so the
    recursion begins at the children.

    O(n) time, O(n) space.
    """

    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        seen = {k - root.val}

        def search(node: Optional[TreeNode]) -> bool:
            if node is None:
                return False

            if node.val in seen:
                return True
            seen.add(k - node.val)
            return search(node.left) or search(node.right)

        return search(root.left) or search(root.right)


class SolutionRecursiveSet:
    """The same walk without the seeding, starting the recursion at the root.

    Nothing is gained or lost against the seeded version — it is the tidier way
    to write it, and measures the same.

    O(n) time, O(n) space.
    """

    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        seen = set()

        def search(node: Optional[TreeNode]) -> bool:
            if not node:
                return False

            if node.val in seen:
                return True
            seen.add(k - node.val)
            return search(node.left) or search(node.right)

        return search(root)


class SolutionSearchPerNode:
    """No complement set: for each node, binary-search the BST for its partner.

    The only approach here that uses the ordering the problem gives. Trades the
    O(n) set for a descent per node, and has to reject the node finding itself —
    which is what ``origin`` guards.

    O(n*h) time with height h, O(h) space.
    """

    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        stack = [root]

        def contains(node: TreeNode, wanted: int, origin: TreeNode) -> bool:
            while node:
                if wanted == node.val and node is not origin:
                    return True
                node = node.left if wanted < node.val else node.right
            return False

        while stack:
            node = stack.pop()
            if contains(root, k - node.val, node):
                return True
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return False


class SolutionQueueSet:
    """Complement trick breadth-first, iterating the queue as it grows.

    ``for node in queue`` walks a list that is still being appended to, which is
    a level-order traversal with no ``pop`` and no ``deque``. Children are
    checked before being appended, so no ``None`` ever enters the queue.

    O(n) time, O(n) space.
    """

    def findTarget(self, root: Optional[TreeNode], k: int) -> bool:
        if not root:
            return False

        seen = set()
        queue = [root]

        for node in queue:
            val = node.val
            if val in seen:
                return True
            seen.add(k - val)

            left = node.left
            right = node.right

            if left:
                queue.append(left)
            if right:
                queue.append(right)

        return False
