"""Cases for 19. Remove Nth Node From End of List.

Declare data only: ``conftest.py`` parametrizes over SOLUTIONS x CASES.
"""

from __future__ import annotations

from typing import Any

from lc.harness import check, load_solutions

SOLUTIONS = load_solutions(__file__)


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
        a: Any = self
        b: Any = other
        while a is not None and b is not None:
            if getattr(a, "val", None) != getattr(b, "val", None):
                return False
            a = getattr(a, "next", None)
            b = getattr(b, "next", None)
        return a is None and b is None


def linked_list(values: list[int]) -> ListNode | None:
    dummy = ListNode()
    curr = dummy
    for v in values:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def NORMALIZE(value: Any) -> list[int]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    vals = []
    curr = value
    while curr:
        vals.append(curr.val)
        curr = curr.next
    return vals


CASES = [
    # Examples
    ((linked_list([1, 2, 3, 4, 5]), 2), [1, 2, 3, 5]),
    ((linked_list([1]), 1), []),
    ((linked_list([1, 2]), 1), [1]),
    # Remove head
    ((linked_list([1, 2]), 2), [2]),
    ((linked_list([1, 2, 3, 4]), 4), [2, 3, 4]),
    # Remove tail
    ((linked_list([1, 2, 3, 4]), 1), [1, 2, 3]),
    # Remove middle
    ((linked_list([1, 2, 3]), 2), [1, 3]),
    # Repeated / boundary values
    ((linked_list([0, 0, 0]), 2), [0, 0]),
    ((linked_list([0, 100]), 1), [0]),
    # Maximum constraint size: sz = 30
    ((linked_list(list(range(1, 31))), 1), list(range(1, 30))),
    ((linked_list(list(range(1, 31))), 30), list(range(2, 31))),
    (
        (linked_list(list(range(1, 31))), 15),
        [x for x in range(1, 31) if x != 16],
    ),
]


def test_solution(solution, case, equal):
    check(solution, case, equal)
