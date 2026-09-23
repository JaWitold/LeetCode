"""88. Merge Sorted Array — https://leetcode.com/problems/merge-sorted-array/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.

The answer is written into ``nums1``, which is the whole difficulty: the space
to write into is the space still holding unread input. Both approaches below
sidestep that rather than solve it — one by sorting, the other by shifting.
"""

ENTRY = "merge"


class SolutionConcatSort:
    """Drop nums2 into the padding and let the sort sort it out.

    Ignores the precondition entirely — the two halves are already sorted, and
    this throws that away. What saves it is that the work happens in C: Timsort
    finds the two existing runs and merges them, so the log factor is never
    really paid on input shaped like this.

    O((m + n) log(m + n)) time, O(m + n) space for the sort's workspace.
    """

    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        nums1[m:] = nums2
        nums1.sort()


class SolutionForwardInsert:
    """Walk forward, inserting each nums2 value at the position it belongs.

    The invariant is that ``nums1[:filled]`` is sorted and holds every value
    consumed so far. Inserting in the middle means shifting everything after it
    one place right, which is the price of going forward: the room at the end of
    ``nums1`` is behind the cursor, not in front of it.

    ``del nums1[m:]`` drops the padding first so the list can grow back by
    insertion — and it truncates in place. Rebinding with ``nums1 = nums1[:m]``
    would build a copy and leave the caller's list untouched, which is the one
    mistake this problem is built to punish.

    O(m * n) time, O(m) space for the slice copy each shift makes.
    """

    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        del nums1[m:]
        if m == 0:
            nums1[:] = nums2
            return

        filled = m
        cursor, taken = 0, 0
        while taken < n:
            if nums1[cursor] < nums2[taken]:
                if cursor < filled - 1:
                    cursor += 1
                else:
                    nums1[filled:] = nums2[taken:]
                    return
            else:
                nums1[cursor + 1 :] = nums1[cursor:]
                nums1[cursor] = nums2[taken]
                filled += 1
                taken += 1
                cursor += 1
        nums1[filled:] = nums2[taken:]


class SolutionBackwardTwoPointer:
    """Fill from the end, where the free space already is.

    The conflict this problem is built around — writing into storage that still
    holds unread input — disappears if the merge runs backwards. Compare the two
    largest unread values and put the winner in the last free slot: the write
    cursor starts at ``m + n - 1`` while the read cursors start at ``m - 1`` and
    ``n - 1``, so the write position is always at or ahead of both and can never
    land on something unread.

    That invariant is what removes the shifting and the extra array at once.
    The loop ends when ``nums2`` is exhausted; anything left in ``nums1`` is
    already below everything written and already in place, so it needs no move.

    O(m + n) time, O(1) space.
    """

    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        write = m + n - 1
        left, right = m - 1, n - 1

        while right >= 0:
            if left >= 0 and nums1[left] > nums2[right]:
                nums1[write] = nums1[left]
                left -= 1
            else:
                nums1[write] = nums2[right]
                right -= 1
            write -= 1
