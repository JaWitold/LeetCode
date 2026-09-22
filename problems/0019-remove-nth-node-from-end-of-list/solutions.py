"""19. Remove Nth Node From End of List — https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.
"""

from __future__ import annotations

ENTRY = "removeNthFromEnd"


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        vals: list[str] = []
        curr: ListNode | None = self
        while curr:
            vals.append(str(curr.val))
            curr = curr.next
        return f"ListNode([{', '.join(vals)}])"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ListNode):
            return False
        a: ListNode | None = self
        b: ListNode | None = other
        while a and b:
            if a.val != b.val:
                return False
            a, b = a.next, b.next
        return a is None and b is None


class SolutionTwoPointers:
    """Two pointers with an n-step delay: advance a fast pointer n steps,
    then step fast and slow together until fast reaches the end. Track the
    node before slow to unlink it, handling head removal when prev is None.

    O(sz) time, O(1) space.
    """

    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        if head is None:
            return None

        fast = slow = head
        prev = None

        for _ in range(n):
            if fast is None:
                break
            fast = fast.next

        while fast is not None:
            fast = fast.next
            prev = slow
            slow = slow.next

        if prev is None:
            head = slow.next if slow is not None else None
        else:
            prev.next = prev.next.next

        return head
