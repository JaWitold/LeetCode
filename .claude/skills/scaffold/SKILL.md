---
name: scaffold
description: Use when the user pastes a LeetCode problem page and wants it set up - creates the problem directory, writes the statement verbatim, and fills CASES before any solution exists.
---

# Scaffolding a problem from a pasted page

Input is whatever the user copied off LeetCode: title line, difficulty, the
statement, examples, constraints, and a tail of page furniture. Turn that into
a ready-to-solve problem directory. Write no solution — cases come first, and
the user writes the approaches.

## 1. Read the paste

Pull out, and ignore everything else:

- **number and title** from the first line (`21. Merge Two Sorted Lists`);
- **difficulty** — the bare word `Easy`/`Medium`/`Hard`, lowercased;
- **topics** — the list under the *second* `Topics` heading at the very bottom
  (`Linked List`, `Recursion`), kebab-cased to `linked-list,recursion`. The
  first `Topics` near the top is a collapsed widget with nothing under it;
- **statement, examples, constraints** — everything from the first prose line
  down to the end of the constraints block.

Discard: `Solved`, `premium lock icon`, `Companies`, `Seen this question in a
real interview before?`, the `1/6` / `Yes` / `No` widget, `Accepted`,
`Acceptance Rate` and the numbers under them.

**The entry method name is not in the paste.** It lives in LeetCode's code
editor, not the description. Infer the conventional name (`mergeTwoLists`,
`twoSum`) and say which you used, or ask when the guess is not obvious — it
must match exactly, since solutions are pasted back.

## 2. Scaffold

```bash
uv run lc new <number> "<Title>" -d <difficulty> -t <topics> -e <entryMethod>
```

Add `--notebook` only if the user asks; a notebook is written later, when
there is something to explain.

## 3. Problem statement, verbatim

Follow `.claude/rules/notes.md`: the statement is copied, never reworded. Apply
only styling and copy artifacts — fence the examples, put `code` around
identifiers, restore flattened superscripts (`104` -> `10^4`), and turn the
constraints into a list.

Two things the paste usually loses:

- **images** — keypad diagrams, tree pictures, linked-list figures. A copied
  page keeps the caption and drops the picture, leaving `Explanation:` with
  nothing under it.

  **Ask for the image URL** rather than inventing a replacement: on LeetCode it
  is reachable by right-clicking the figure, and looks like
  `https://assets.leetcode.com/uploads/2020/10/03/swap_ex1.jpg`. Embed it with
  alt text that describes what it shows, so the README still reads with images
  off:

  ```markdown
  ![Example 1: the list 1 -> 2 -> 3 -> 4 becomes 2 -> 1 -> 4 -> 3](https://assets.leetcode.com/uploads/2020/10/03/swap_ex1.jpg)
  ```

  Only when the user cannot supply it, reproduce the content as a fenced block
  or table — and say in your reply that you did, since it is the one place you
  added text rather than copied it.
- **example figures** — "Example 1:" followed by a blank line where a picture
  was. Keep the input/output block that follows it.

## 4. Fix the stub signature

`lc new` writes `def <entry>(self):` with no parameters. Give it the argument
list and return type LeetCode declares, so a case fails with
`NotImplementedError` rather than a `TypeError` about arity.

## 5. Structured inputs need a builder

Linked lists and trees arrive as bracket notation (`[1,2,4]`,
`[5,3,6,2,4,null,7]`). Put the node class and the builder **in the test
module** — `linked_list(values)`, `tree(values)` — with a `__repr__` that
prints the bracket form, so pytest ids stay readable. Give the solutions file
the node class LeetCode defines in its editor, exactly as it writes it.

The two are separate classes on purpose: the solutions file is what gets pasted
back to the judge, and duck typing means the harness does not care that they
differ.

## 6. CASES, before any solution

Per `.claude/rules/testing.md`, and in this order:

1. every example from the statement;
2. the boundaries the constraints permit — empty input when the constraints
   allow it (read them: `[0, 50]` nodes allows an empty list, `1 <=` does not),
   single element, all-equal values, both extremes of the value range;
3. the shape that catches the mistake this problem invites — a duplicate that
   is not part of the answer, an element that would pair with itself, a
   dedup skip that is too eager;
4. one input at the constraint's size limit, unless a brute-force approach
   would then hang the suite rather than fail it. Say so in your reply when you
   cap it lower.

**Compute every expected value with a reference implementation before writing
it down**, and say in your reply that you did. A case that encodes a guess is
worse than no case. When the answer's order is free, define `NORMALIZE`;
when the answer is a count or a single value, compare directly.

## 7. Hand back

Run `uv run pytest problems/<dir>` and confirm the cases fail against the stub —
that is the intended state. Then `uv run lc index`, `uv run ruff format .` and
`uv run ruff check .`.

Report: the case table (what each one guards), anything you inferred rather
than copied, and anything you deliberately left out.
