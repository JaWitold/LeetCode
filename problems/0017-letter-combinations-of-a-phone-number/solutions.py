"""17. Letter Combinations of a Phone Number — https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Each approach is its own ``Solution*`` class; the test module runs every one of
them against every case.

Both are the same recursion — prefix every combination of the tail with each
letter of the head digit — written as a comprehension. They differ only in
which of the two ``for`` clauses comes first, and that decides whether the
recursive call is evaluated once per level or once per letter.
"""

ENTRY = "letterCombinations"


class SolutionRecursiveSuffixPerLetter:
    """Letters outer, recursion inner — so the tail is rebuilt for every letter.

    A comprehension re-evaluates its inner iterable for each item of the outer
    one. With ``for letter ... for suffix in self.letterCombinations(...)`` the
    recursive call sits in the inner clause, so the whole tail is recomputed
    from scratch once per letter of the head digit, and the recursion tree
    branches instead of running straight down: 341 calls for four digits where
    the other approach makes 5, and 87,381 against 9 at eight digits.

    O(n^2 * 4^n) time, O(4^n) space for the answer.
    """

    def letterCombinations(self, digits: str) -> list[str]:
        keypad = {
            "2": ["a", "b", "c"],
            "3": ["d", "e", "f"],
            "4": ["g", "h", "i"],
            "5": ["j", "k", "l"],
            "6": ["m", "n", "o"],
            "7": ["p", "q", "r", "s"],
            "8": ["t", "u", "v"],
            "9": ["w", "x", "y", "z"],
        }

        if digits == "":
            return [""]

        return [
            f"{letter}{suffix}"
            for letter in keypad[digits[0]]
            for suffix in self.letterCombinations(digits[1:])
        ]


class SolutionRecursiveSuffixOnce:
    """Recursion outer, letters inner — the tail is computed once per level.

    Swapping the two clauses moves the recursive call into the outer position,
    where a comprehension evaluates it exactly once. The recursion then walks
    straight down the string, one call per digit, and each level prefixes the
    tail it already has.

    The empty string returning ``[""]`` is the identity the recursion needs:
    the tail of the last digit contributes one empty suffix to prefix onto. It
    is unreachable from outside, since the constraints give at least one digit.

    O(n * 4^n) time, O(4^n) space for the answer.
    """

    def letterCombinations(self, digits: str) -> list[str]:
        keypad = {
            "2": ["a", "b", "c"],
            "3": ["d", "e", "f"],
            "4": ["g", "h", "i"],
            "5": ["j", "k", "l"],
            "6": ["m", "n", "o"],
            "7": ["p", "q", "r", "s"],
            "8": ["t", "u", "v"],
            "9": ["w", "x", "y", "z"],
        }

        if digits == "":
            return [""]

        return [
            f"{letter}{suffix}"
            for suffix in self.letterCombinations(digits[1:])
            for letter in keypad[digits[0]]
        ]
