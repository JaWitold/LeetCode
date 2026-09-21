"""18. 4Sum — https://leetcode.com/problems/4sum/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.

Both are 3Sum's answer with one more loop wrapped around it: pin the two
smallest members, two-pointer the rest, and jump the pointers with a binary
search. They differ only in what collects the answer.
"""

from bisect import bisect_left, bisect_right

ENTRY = "fourSum"


class SolutionBisectJumpSet:
    """Pin two, two-pointer the rest, and let a set absorb repeated quadruplets.

    The pruning is what makes the cubic bound bearable: a pinned pair whose two
    smallest partners already overshoot ends the loop, and one whose two largest
    partners still fall short is skipped. The same test runs one level up on the
    first pin.

    The set is belt and braces — the equal-value skips on all four positions
    already make each quadruplet reachable once, as `SolutionBisectJumpList`
    relies on.

    O(n^3) time, O(t) space for t quadruplets.
    """

    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        quadruplets = set()
        n = len(nums)

        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            if nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break

            if nums[i] + nums[n - 1] + nums[n - 2] + nums[n - 3] < target:
                continue

            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue

                pinned = nums[i] + nums[j]

                if pinned + nums[j + 1] + nums[j + 2] > target:
                    break

                if pinned + nums[n - 1] + nums[n - 2] < target:
                    continue

                left = j + 1
                right = n - 1
                while left < right:
                    total = pinned + nums[left] + nums[right]

                    if total == target:
                        quadruplets.add((nums[i], nums[j], nums[left], nums[right]))
                        left += 1
                        right -= 1
                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
                    elif total < target:
                        left = bisect_left(nums, target - pinned - nums[right], left + 1, right)
                    else:
                        right = bisect_right(nums, target - pinned - nums[left], left, right - 1)
        return [list(quadruplet) for quadruplet in quadruplets]


class SolutionBisectJumpList:
    """The same scan, appending to a list and trusting the skips to dedupe.

    Each of the four positions steps over equal values, so a quadruplet can be
    produced only once — the set in the other approach never removes anything.
    Dropping it also keeps the answer in sorted order rather than a set's
    arbitrary one.

    O(n^3) time, O(1) space excluding the output.
    """

    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        quadruplets = []
        n = len(nums)

        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            if nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break

            if nums[i] + nums[n - 1] + nums[n - 2] + nums[n - 3] < target:
                continue

            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue

                pinned = nums[i] + nums[j]

                if pinned + nums[j + 1] + nums[j + 2] > target:
                    break

                if pinned + nums[n - 1] + nums[n - 2] < target:
                    continue

                left = j + 1
                right = n - 1
                while left < right:
                    total = pinned + nums[left] + nums[right]

                    if total == target:
                        quadruplets.append([nums[i], nums[j], nums[left], nums[right]])
                        left += 1
                        right -= 1
                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
                    elif total < target:
                        left = bisect_left(nums, target - pinned - nums[right], left + 1, right)
                    else:
                        right = bisect_right(nums, target - pinned - nums[left], left, right - 1)
        return quadruplets
