"""167. Two Sum II - Input Array Is Sorted — https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.

The classes are in the order they were written, from the Two Sum leftover that
ignores the sorted input to the run-skipping bisect that exploits it fully.
"""

from bisect import bisect_left, bisect_right

ENTRY = "twoSum"


class SolutionHashMap:
    """Two Sum's answer, carried over: remember the complement each element waits for.

    Correct, but it throws the sorted input away and pays O(n) memory for it —
    the problem explicitly asks for constant extra space.

    O(n) time, O(n) space.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for index, value in enumerate(numbers):
            if value in seen:
                return [seen[value] + 1, index + 1]
            seen[target - value] = index
        return []


# class SolutionScanForComplement:
#     """For each left index, walk right while the values can still reach the complement.
#
#     Sortedness is used only to stop early: the scan breaks once values exceed
#     the complement. When the complement is larger than everything to the right —
#     a long run of small values — nothing is pruned and the scan is full length.
#
#     O(n^2) time, O(1) space.
#     """
#
#     def twoSum(self, numbers: list[int], target: int) -> list[int]:
#         length = len(numbers)
#         for left in range(length - 1):
#             complement = target - numbers[left]
#
#             right = left + 1
#             while right < length and numbers[right] <= complement:
#                 if numbers[right] == complement:
#                     return [left + 1, right + 1]
#
#                 right += 1
#         return []


class SolutionTwoPointers:
    """The textbook walk inwards from both ends, one step at a time.

    If the sum is too small, no pair using the current left value can work —
    every partner is at or left of the current right — so left may advance, and
    symmetrically for right. Each step discards exactly one candidate.

    O(n) time, O(1) space.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]

            if total < target:
                left += 1
            else:
                right -= 1
        return []


class SolutionTwoPointersSkipImpossible:
    """Same walk, but each step skips every index that cannot pair with the other end.

    The inner loops run to the first left value large enough for the current
    right partner, and to the last right value small enough for the current left
    partner. Pointers still only move inwards, so the total work is unchanged;
    what changes is that a run is crossed in one outer iteration.

    O(n) time, O(1) space.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            low_value = numbers[left]
            high_value = numbers[right]
            if target - low_value - high_value == 0:
                return [left + 1, right + 1]

            while numbers[left] < target - high_value:
                left += 1
            while numbers[right] > target - low_value:
                right -= 1
        return []


class SolutionTwoPointersSkipDuplicates:
    """Two pointers that step over a repeated value instead of re-testing it.

    Once a value has been rejected against the other end, every copy of it is
    rejected too, so the pointer runs to the end of the run. Same O(n) bound as
    the plain walk, but a wall of duplicates costs one comparison per element
    rather than one full loop iteration.

    O(n) time, O(1) space.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            gap = target - numbers[left] - numbers[right]
            if gap == 0:
                return [left + 1, right + 1]

            if gap > 0:
                left += 1
                while numbers[left] == numbers[left - 1]:
                    left += 1
            else:
                right -= 1
                while numbers[right] == numbers[right + 1]:
                    right -= 1
        return []


class SolutionBisectJump:
    """Two pointers, but each move jumps straight to the first useful index.

    Instead of walking, binary-search the position where the value could reach
    the target with the opposite end. Every outer iteration then consumes at
    least one *distinct* value; with values bounded to -1000..1000 that is at
    most 2001 iterations however long the array is.

    O(d log n) time with d distinct values, O(1) space.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]

            if total < target:
                # first index whose value is large enough to pair with `right`
                left = bisect_left(numbers, target - numbers[right], left + 1, right)
            else:
                # last index whose value is small enough to pair with `left`
                right = bisect_right(numbers, target - numbers[left], left, right) - 1

        return []


class SolutionMidpointProbe:
    """Hand-rolled halving: one probe per move, jumping only inside a run.

    If the midpoint holds the same value as the pointer, the whole span up to it
    is that same value and can be skipped in one move; otherwise fall back to a
    single step. Cheap on long runs, but a single probe does not find the end of
    the run, so it can take many iterations to cross one.

    O(n) time worst case, O(1) space.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            gap = target - numbers[left] - numbers[right]
            if gap == 0:
                return [left + 1, right + 1]

            midpoint = (left + right) // 2

            if gap > 0:
                if numbers[midpoint] == numbers[left]:
                    left = midpoint
                else:
                    left += 1
            else:
                if numbers[midpoint] == numbers[right]:
                    right = midpoint
                else:
                    right -= 1
        return []


class SolutionBisectRunEnd:
    """Binary-search the end of the run of equal values, by hand.

    Each move lands on the first index past every copy of the value just
    rejected, so one outer iteration consumes one distinct value. The searches
    are written out rather than taken from ``bisect`` because the predicate is
    "still equal to this value", not an ordering comparison.

    The flip side: on all-distinct input every run has length one, so each
    binary search pays O(log n) to advance a single index and the whole thing
    is slower than the plain walk. The value range in the constraints caps d at
    2001, which is why the judge never sees that case.

    O(d log n) time with d distinct values, O(1) space.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        def run_end(lo: int, hi: int, value: int) -> int:
            """First index at or after ``lo`` that no longer holds ``value``."""
            while lo < hi:
                midpoint = (lo + hi) // 2
                if numbers[midpoint] == value:
                    lo = midpoint + 1
                else:
                    hi = midpoint - 1
            return lo

        def run_start(lo: int, hi: int, value: int) -> int:
            """Last index at or before ``hi`` that no longer holds ``value``."""
            while lo < hi:
                midpoint = (lo + hi) // 2
                if numbers[midpoint] == value:
                    hi = midpoint - 1
                else:
                    lo = midpoint + 1
            return hi

        left = 0
        right = len(numbers) - 1
        while left < right:
            gap = target - numbers[left] - numbers[right]
            if gap == 0:
                return [left + 1, right + 1]

            if gap > 0:
                left = run_end(left + 1, right, numbers[left])
            else:
                right = run_start(left, right - 1, numbers[right])
        return []


class SolutionInlineBisectJump:
    """The bisect jump with the searches written out, and no stdlib call.

    Same move as :class:`SolutionBisectJump` — jump to the first index whose
    value could still reach the target with the opposite end — but the binary
    search is inlined, so there is no function call and no slice bookkeeping per
    step.

    The searches look off by one, and deliberately so: closing with ``mid - 1``
    and ``mid + 1`` on both sides means the landing index can stop *short* of the
    true boundary, never past it. ``lo`` only advances from a probe that is
    strictly below the needed value, so it can never skip the answer; the cost
    of a conservative landing is an extra outer iteration, not a wrong result.

    O(d log n) time with d distinct values, O(1) space.
    """

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]
            if current_sum == target:
                return [left + 1, right + 1]

            if current_sum < target:
                needed = target - numbers[right]
                lo, hi = left + 1, right
                while lo < hi:
                    probe = (lo + hi) // 2
                    if numbers[probe] >= needed:
                        hi = probe - 1
                    else:
                        lo = probe + 1
                left = lo
            else:
                needed = target - numbers[left]
                lo, hi = left, right - 1
                while lo < hi:
                    probe = (lo + hi) // 2
                    if numbers[probe] <= needed:
                        lo = probe + 1
                    else:
                        hi = probe - 1
                right = hi
        return []
