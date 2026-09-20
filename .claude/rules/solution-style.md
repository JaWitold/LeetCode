# Solution style

- One class per approach, named for the technique (`SolutionHashMap`,
  `SolutionTwoPointers`), ordered simplest-first in the file. A faster approach
  is added alongside the old one, never in place of it.
- Signatures stay exactly as LeetCode gives them, including `camelCase` method
  names — solutions are pasted back. `ENTRY = "<methodName>"` at module level
  names the method for the harness; it is only optional when the class has a
  single public method.
- Type-annotate parameters and return. Standard library only, and only what
  LeetCode's judge has (`collections`, `heapq`, `bisect`, `functools`, `math`).
- **Every `Solution*` class states both its time and its space complexity — no
  exceptions, not even for a brute force.** Two places, same claim:
  - last line of the class docstring: `O(n) time, O(n) space.`
  - the approach's README subsection, as a two-line block with the reason:

    ```markdown
    - **Time:** O(n) — one pass over `nums`
    - **Space:** O(n) — the map holds at most one entry per element
    ```

  The reason after the dash is part of the template: a bare `O(n)` is not
  enough. Give the worst case unless stated otherwise, count space *excluding*
  the output, and when an approach is faster than its complexity suggests (work
  pushed into C, early exit) say so there rather than quietly claiming a better
  class.
- Class docstring otherwise carries the invariant that makes the approach
  correct. Inline comments are for the non-obvious step only
  (why the store happens *after* the look-up, why the pop needs a guard).
- No I/O, no printing, no mutation of module state. Solutions may mutate their
  arguments — the harness deep-copies inputs per run.
