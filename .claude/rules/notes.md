# Notes

Each problem's `README.md` opens with front matter (`number`, `title`,
`difficulty`, `topics`, `url`, `status`) that `lc index` reads to build the root
progress table — keep the keys intact and rerun `uv run lc index` after editing.

The body is written for the reader who has forgotten the problem:

- **Problem** — **copied verbatim from LeetCode. Never reword, summarize or
  "improve" it**, and never replace it with a restatement; the wording is the
  specification. Permitted edits are only:
  - markdown styling: paragraph breaks, `code` around identifiers such as
    `nums` and `target`, lists, and examples in a fenced block;
  - artifacts of copying, where a superscript was flattened: `104` -> `10^4`,
    `109` -> `10^9`, `231` -> `2^31`, `n2` -> `n^2`.

  Copy the Constraints block too when it is there — it is what decides which
  complexity is acceptable. Anything you want to add in your own words belongs
  under Approaches or Notes.
- **Approaches** — one subsection per `Solution*` class, in file order. Lead with
  the idea and the invariant, not a line-by-line paraphrase of the code, and end
  with time and space.
- **Edge cases** — what the `CASES` are guarding, and which solution each one
  would have caught.
- **Notes** — what went wrong on the first attempt, the transferable trick, and
  links to related problems.
