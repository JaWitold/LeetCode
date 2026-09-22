"""21. Merge Two Sorted Lists — https://leetcode.com/problems/merge-two-sorted-lists/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.
"""

ENTRY = "mergeTwoLists"


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SolutionBrute:
    """<Invariant that makes this correct.>

        O(n + m) time, O(1) space.
        Runtime
    0
    ms
    Beats
    100.00%
    Memory
    19.22
    MB
    Beats
    74.13%

    """

    def mergeTwoLists(self, list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
        current = head = ListNode()

        while list1 is not None and list2 is not None:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next

        current.next = list1 if list1 is not None else list2
        return head.next
