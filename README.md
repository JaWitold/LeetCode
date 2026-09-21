# LeetCode

Solutions, notes, tests and notebooks. One directory per problem; every approach
kept side by side and tested against the same cases.

```
problems/NNNN-slug/
  README.md          notes: restatement, approaches, complexity, edge cases
  solutions.py       one Solution* class per approach
  test_<slug>.py     CASES only — conftest.py runs every solution against every case
  explain.ipynb      derivation + traces (hard problems only)
```

## Usage

```bash
uv sync                                    # install dev tooling
uv run lc new 704 "Binary Search" -d easy -t array,binary-search -e search
uv run pytest                              # all problems
uv run pytest problems/NNNN-slug           # one problem
uv run pytest -k SolutionHashMap           # one approach
uv run lc bench 42                         # time approaches against each other
uv run lc index                            # regenerate the table below
uv run lc pycharm                          # (re)generate PyCharm run configurations
uv run lc nb                               # strip notebook outputs before committing
uv run ruff check . && uv run ruff format .
```

Adding an approach means adding a `Solution*` class to `solutions.py` — the test
suite picks it up with no new test code.

## Progress

<!-- lc:index:start -->
| # | Problem | Difficulty | Topics | Approaches | Notes |
|---|---------|------------|--------|------------|-------|
| 1 | [Two Sum](problems/0001-two-sum/README.md) | easy | junior, array, hash-table | NestedLoops, NestedLoopsSkipRepeats, ComplementScan, ComplementHashMap | notebook |
| 15 | [3Sum](problems/0015-3sum/README.md) | medium | array, two-pointers-sorting | MiddlePivotSet, TwoPointersPruned, BisectJump | notebook |
| 18 | [4Sum](problems/0018-4sum/README.md) | medium | array, two-pointers, sorting | BisectJumpSet, BisectJumpList | notebook |
| 167 | [Two Sum II - Input Array Is Sorted](problems/0167-two-sum-ii-input-array-is-sorted/README.md) | medium | array, two-pointers, binary-search | HashMap, TwoPointers, TwoPointersSkipImpossible, TwoPointersSkipDuplicates, BisectJump, MidpointProbe, BisectRunEnd, InlineBisectJump | notebook |
| 653 | [Two Sum IV - Input is a BST](problems/0653-two-sum-iv-input-is-a-bst/README.md) | easy | mid-level, hash-table, two-pointers, tree, depth-first-search, breadth-first-search, binary-search-tree, binary-tree | RecursiveList, StackSet, RecursiveSetSeeded, RecursiveSet, SearchPerNode, QueueSet | notebook |
<!-- lc:index:end -->
