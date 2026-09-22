"""454. 4Sum II — https://leetcode.com/problems/4sum-ii/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.

Seven of the eight share one invariant: split the four arrays into two pairs,
build a frequency map of every pairwise sum from the first pair, then scan the
second pair and look up each negated sum. The first does not split at all — it
loops over three arrays and looks the fourth value up — which is what makes it
the slow one. The rest differ only in how they build the per-value frequency
counts and whether they materialise the second pair's sums into a dict or
accumulate directly.

u = number of distinct values per array; u ≤ n.
"""

from collections import Counter

ENTRY = "fourSumCount"


class SolutionTripleLoop:
    """Iterate all unique triples (a, b, c) from nums1×nums2×nums3 and look up
    whether -(a+b+c) is present in nums4. The one approach here that does not
    split the arrays into two pairs, and the only one that is not quadratic.

    As submitted, the membership test read ``in set(nums4)``, rebuilding that
    set on every innermost iteration — an O(n) "lookup" that made the whole
    thing O(u³·n), 12x slower at u=10 and 17x at u=40. The sets are now built
    once, which is what the O(1) lookup claim needed all along.

    O(n·u + u³) time, O(u) space.
    """

    def fourSumCount(
        self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]
    ) -> int:
        vals1, vals2 = set(nums1), set(nums2)
        vals3, vals4 = set(nums3), set(nums4)

        freq1 = {a: nums1.count(a) for a in vals1}
        freq2 = {b: nums2.count(b) for b in vals2}
        freq3 = {c: nums3.count(c) for c in vals3}
        freq4 = {d: nums4.count(d) for d in vals4}

        total = 0

        for a in vals1:
            for b in vals2:
                for c in vals3:
                    need = -a - b - c
                    if need in vals4:
                        total += freq1[a] * freq2[b] * freq3[c] * freq4[need]
        return total


class SolutionSplitPairCount:
    """Split into two halves: build sums12 over nums1×nums2, sums34 over
    nums3×nums4, then join. Per-value frequencies are computed with
    list.count() inside the pairing loops — once per unique pair (a, b), so
    list.count() on nums2 is called u1×u2 times rather than u2 times.

    O(u²·n) time, O(u²) space.
    """

    def fourSumCount(
        self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]
    ) -> int:
        sums12 = {}
        for a in set(nums1):
            cnt_a = nums1.count(a)

            for b in set(nums2):
                cnt_b = nums2.count(b)

                if a + b in sums12:
                    sums12[a + b] += cnt_a * cnt_b
                else:
                    sums12[a + b] = cnt_a * cnt_b

        sums34 = {}
        for c in set(nums3):
            cnt_c = nums3.count(c)

            for d in set(nums4):
                cnt_d = nums4.count(d)

                if c + d in sums34:
                    sums34[c + d] += cnt_c * cnt_d
                else:
                    sums34[c + d] = cnt_c * cnt_d

        total = 0

        for s in sums12:
            if -s in sums34:
                total += sums12[s] * sums34[-s]
        return total


class SolutionSplitAllCount:
    """Same two-phase split as SolutionSplitPairCount, but the four frequency
    maps are populated in a single range loop before pairing. list.count() is
    still called once per element index — n calls per array, each O(n) — so
    repeated values trigger redundant rescans.

    O(n²) time, O(u²) space.
    """

    def fourSumCount(
        self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]
    ) -> int:
        freq1, freq2, freq3, freq4 = {}, {}, {}, {}
        n = len(nums1)
        for i in range(n):
            freq1[nums1[i]] = nums1.count(nums1[i])
            freq2[nums2[i]] = nums2.count(nums2[i])
            freq3[nums3[i]] = nums3.count(nums3[i])
            freq4[nums4[i]] = nums4.count(nums4[i])

        sums12 = {}
        for a in set(nums1):
            for b in set(nums2):
                if a + b not in sums12:
                    sums12[a + b] = 0

                sums12[a + b] += freq1[a] * freq2[b]

        sums34 = {}
        for c in set(nums3):
            for d in set(nums4):
                if c + d not in sums34:
                    sums34[c + d] = 0

                sums34[c + d] += freq3[c] * freq4[d]

        total = 0

        for s in sums12:
            if -s in sums34:
                total += sums12[s] * sums34[-s]
        return total


class SolutionSplitGuardedCount:
    """Same as SolutionSplitAllCount but a membership check prevents calling
    list.count() more than once per unique value. Each unique value is counted
    exactly once, making the freq-build O(n·u) instead of O(n²).

    O(n·u + u²) time, O(u²) space.
    """

    def fourSumCount(
        self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]
    ) -> int:
        freq1, freq2, freq3, freq4 = {}, {}, {}, {}
        n = len(nums1)
        for i in range(n):
            a, b, c, d = nums1[i], nums2[i], nums3[i], nums4[i]

            if a not in freq1:
                freq1[a] = nums1.count(a)
            if b not in freq2:
                freq2[b] = nums2.count(b)
            if c not in freq3:
                freq3[c] = nums3.count(c)
            if d not in freq4:
                freq4[d] = nums4.count(d)

        sums12 = {}
        for a in set(nums1):
            for b in set(nums2):
                if a + b not in sums12:
                    sums12[a + b] = 0

                sums12[a + b] += freq1[a] * freq2[b]

        sums34 = {}
        for c in set(nums3):
            for d in set(nums4):
                if c + d not in sums34:
                    sums34[c + d] = 0

                sums34[c + d] += freq3[c] * freq4[d]

        total = 0

        for s in sums12:
            if -s in sums34:
                total += sums12[s] * sums34[-s]
        return total


class SolutionSplitSetCount:
    """Build the four unique-value sets explicitly first, then call
    list.count() once per unique value. Equivalent to SolutionSplitGuardedCount
    but the deduplication is expressed upfront via set() rather than lazily via
    a membership guard.

    O(n·u + u²) time, O(u²) space.
    """

    def fourSumCount(
        self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]
    ) -> int:
        freq1, freq2, freq3, freq4 = {}, {}, {}, {}

        vals1 = set(nums1)
        vals2 = set(nums2)
        vals3 = set(nums3)
        vals4 = set(nums4)

        for a in vals1:
            freq1[a] = nums1.count(a)
        for b in vals2:
            freq2[b] = nums2.count(b)
        for c in vals3:
            freq3[c] = nums3.count(c)
        for d in vals4:
            freq4[d] = nums4.count(d)

        sums12 = {}
        for a in vals1:
            for b in vals2:
                if a + b not in sums12:
                    sums12[a + b] = 0

                sums12[a + b] += freq1[a] * freq2[b]

        sums34 = {}
        for c in vals3:
            for d in vals4:
                if c + d not in sums34:
                    sums34[c + d] = 0

                sums34[c + d] += freq3[c] * freq4[d]

        total = 0

        for s in sums12:
            if -s in sums34:
                total += sums12[s] * sums34[-s]
        return total


class SolutionSplitPruned:
    """Same as SolutionSplitSetCount but sums34 is built with pruning: a
    (c, d) pair whose negated sum is absent from sums12 cannot contribute to
    the total, so it is skipped with ``continue``. This avoids populating
    sums34 with entries that the final join would ignore anyway.

    O(n·u + u²) time, O(u²) space — the frequency build is u calls to
    list.count(), each O(n), and dominates whenever u is much smaller than n.
    """

    def fourSumCount(
        self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]
    ) -> int:
        freq1, freq2, freq3, freq4 = {}, {}, {}, {}

        vals1 = set(nums1)
        vals2 = set(nums2)
        vals3 = set(nums3)
        vals4 = set(nums4)

        for a in vals1:
            freq1[a] = nums1.count(a)
        for b in vals2:
            freq2[b] = nums2.count(b)
        for c in vals3:
            freq3[c] = nums3.count(c)
        for d in vals4:
            freq4[d] = nums4.count(d)

        sums12 = {}
        for a in vals1:
            for b in vals2:
                if a + b not in sums12:
                    sums12[a + b] = 0
                sums12[a + b] += freq1[a] * freq2[b]

        sums34 = {}
        for c in vals3:
            for d in vals4:
                need = -c - d
                if need not in sums12:
                    continue
                if need not in sums34:
                    sums34[need] = 0

                sums34[need] += freq3[c] * freq4[d]

        total = 0

        for s in sums12:
            if s in sums34:
                total += sums12[s] * sums34[s]
        return total


class SolutionSplitDirect:
    """Skips building sums34 entirely. For each unique (c, d) pair, look up
    -(c+d) in sums12 and accumulate directly into the total. One fewer dict
    allocation and one fewer pass over the data.

    O(n·u + u²) time, O(u²) space — same frequency build as above.
    """

    def fourSumCount(
        self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]
    ) -> int:
        freq1, freq2, freq3, freq4 = {}, {}, {}, {}

        vals1 = set(nums1)
        vals2 = set(nums2)
        vals3 = set(nums3)
        vals4 = set(nums4)

        for a in vals1:
            freq1[a] = nums1.count(a)
        for b in vals2:
            freq2[b] = nums2.count(b)
        for c in vals3:
            freq3[c] = nums3.count(c)
        for d in vals4:
            freq4[d] = nums4.count(d)

        sums12 = {}
        for a in vals1:
            for b in vals2:
                s = a + b
                if s not in sums12:
                    sums12[s] = 0
                sums12[s] += freq1[a] * freq2[b]

        total = 0
        for c in vals3:
            for d in vals4:
                need = -c - d
                if need not in sums12:
                    continue
                total += sums12[need] * freq3[c] * freq4[d]

        return total


class SolutionSplitCounter:
    """Counter builds each frequency map in a single O(n) pass, replacing the
    set() + list.count() pattern used in the classes above. The two-phase split
    is otherwise identical to SolutionSplitDirect, and dropping the O(n·u)
    frequency build to a single O(n) pass is what makes it the fastest of the
    eight on every shape measured.

    O(n + u²) time, O(u²) space — n² only when every value is distinct.
    """

    def fourSumCount(
        self, nums1: list[int], nums2: list[int], nums3: list[int], nums4: list[int]
    ) -> int:
        freq1 = Counter(nums1)
        freq2 = Counter(nums2)
        freq3 = Counter(nums3)
        freq4 = Counter(nums4)

        sums12 = {}
        for a, cnt_a in freq1.items():
            for b, cnt_b in freq2.items():
                s = a + b
                sums12[s] = sums12.get(s, 0) + cnt_a * cnt_b

        total = 0
        freq4_items = list(freq4.items())

        for c, cnt_c in freq3.items():
            for d, cnt_d in freq4_items:
                need = -c - d
                if need in sums12:
                    total += sums12[need] * cnt_c * cnt_d

        return total
