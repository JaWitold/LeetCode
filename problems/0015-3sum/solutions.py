"""15. 3Sum — https://leetcode.com/problems/3sum/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.

All three sort first and then fix one element and two-pointer the rest — the
question each answers differently is *which* element to fix, and how to avoid
reporting the same triplet twice.
"""

from bisect import bisect_left, bisect_right

ENTRY = "threeSum"


class SolutionMiddlePivotSet:
    """Fix the middle element, close in from both ends, dedupe with a set.

    Sorting makes the two-pointer move legal, but fixing the *middle* element
    means the pointers start outside it and a triplet can be reached by several
    pivots, so duplicates are unavoidable in the scan. A set of tuples absorbs
    them, which costs memory proportional to the answer instead of the O(1) the
    other two need.

    O(n^2) time, O(t) space for t triplets.
    """

    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        triplets = set()
        for pivot in range(1, len(nums) - 1):
            left = 0
            right = len(nums) - 1
            pivot_value = nums[pivot]

            while left < pivot < right:
                total = nums[left] + pivot_value + nums[right]
                if total == 0:
                    triplets.add((nums[left], pivot_value, nums[right]))

                if total < 0:
                    left += 1
                    while left < pivot and nums[left] == nums[left - 1]:
                        left += 1
                else:
                    right -= 1
                    while pivot < right and nums[right] == nums[right + 1]:
                        right -= 1
        return [list(triplet) for triplet in triplets]


class SolutionTwoPointersPruned:
    """Fix the smallest element, then two-pointer the suffix. The textbook answer.

    Fixing the *first* element is what removes the need for a set: the suffix is
    searched once per distinct first value, so a triplet can only be produced by
    the pivot that is its smallest member. Skipping equal values on all three
    positions is then enough to keep the answer unique.

    Three prunes ride on the sort: a positive first value ends the search, a
    first value whose two smallest partners already overshoot ends it too, and
    one whose two largest partners still fall short is skipped.

    O(n^2) time, O(1) space excluding the output.
    """

    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        triplets = []
        n = len(nums)

        for i in range(n - 2):
            value = nums[i]
            if value > 0:
                break

            if i > 0 and value == nums[i - 1]:
                continue

            if value + nums[i + 1] + nums[i + 2] > 0:
                break

            if value + nums[n - 1] + nums[n - 2] < 0:
                continue

            left = i + 1
            right = n - 1
            target = -value

            while left < right:
                total = nums[left] + nums[right]

                if total == target:
                    triplets.append([value, nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif total < target:
                    left += 1
                else:
                    right -= 1
        return triplets


class SolutionBisectJump:
    """The same walk, but each pointer jumps to the first index that could work.

    Instead of stepping one index at a time, binary-search the position where the
    partner value would sit. A run of equal values is crossed in one move, which
    is the same trick as in 167 — and the reason it matters here is that the
    inner walk runs once per distinct first value, so every index skipped is
    skipped n times over.

    O(n^2 log n) worst case, O(1) space excluding the output.
    """

    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        triplets = []
        n = len(nums)

        for i in range(n - 2):
            value = nums[i]
            if value > 0:
                break

            if i > 0 and value == nums[i - 1]:
                continue

            if value + nums[i + 1] + nums[i + 2] > 0:
                break

            if value + nums[n - 1] + nums[n - 2] < 0:
                continue

            left = i + 1
            right = n - 1
            target = -value

            while left < right:
                total = nums[left] + nums[right]

                if total == target:
                    triplets.append([value, nums[left], nums[right]])
                    left += 1
                    right -= 1
                    # compare against where the pointer came from, not where it is going
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif total < target:
                    left = bisect_left(nums, target - nums[right], left + 1, right)
                else:
                    right = bisect_right(nums, target - nums[left], left, right - 1)
        return triplets
