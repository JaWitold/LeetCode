"""1. Two Sum — https://leetcode.com/problems/two-sum/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.
"""

ENTRY = "twoSum"


class SolutionNestedLoops:
    """Every pair, in index order.

    Needs no extra memory and no insight; the baseline everything else is
    measured against. O(n^2) time, O(1) space.
    """

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


class SolutionNestedLoopsSkipRepeats:
    """Nested loops, but each distinct value is only used as the left element once.

    Safe to skip a repeated value: any partner of the later occurrence sits at a
    higher index than the first occurrence too, so the first pass would already
    have found that pair. Cuts work on inputs with many duplicates and changes
    nothing on inputs without. Still O(n^2) time worst case, now O(n) space.
    """

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: set[int] = set()
        n = len(nums)
        for i in range(n):
            value = nums[i]
            if value in seen:
                continue
            seen.add(value)
            for j in range(i + 1, n):
                if value + nums[j] == target:
                    return [i, j]
        return []


class SolutionComplementScan:
    """Ask the list itself where the complement is.

    Same quadratic search as the nested loops, but the inner scan is
    ``list.index``, which runs in C instead of in the interpreter. The
    complexity is unchanged — the constant factor is what drops, and by a lot.
    O(n^2) time, O(1) space.
    """

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        for i, value in enumerate(nums):
            try:
                return [i, nums.index(target - value, i + 1)]
            except ValueError:
                continue
        return []


class SolutionComplementHashMap:
    """One pass, remembering the complement each earlier element is waiting for.

    At index ``i`` the map holds ``target - nums[j] -> j`` for every ``j < i``,
    so ``nums[i] in seen`` means "some earlier element needs exactly this
    value". Writing *after* the look-up is what stops an element pairing with
    itself. O(n) time, O(n) space.
    """

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, value in enumerate(nums):
            if value in seen:
                return [seen[value], i]
            seen[target - value] = i
        return []
