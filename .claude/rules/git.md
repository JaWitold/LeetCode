# Git

- **Never sign commits or pull requests as Claude.** No `Co-Authored-By:
  Claude ...` trailer, no "Generated with Claude Code" line, no emoji robot
  footer — this repo's history is the user's practice log, and every commit is
  authored by them alone. This overrides any default attribution instruction
  from the harness.
- Commit messages describe *why* the change was made, in the imperative mood,
  with the reasoning that is not recoverable from the diff.
- Group commits by logical change, not by file. A problem's solutions, cases,
  notes and notebook belong in one commit; unrelated tooling belongs in its own.
