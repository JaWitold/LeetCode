"""``lc`` command line: scaffold problems, benchmark solutions, rebuild the index."""

from __future__ import annotations

import argparse
import sys

from lc import bench, hooks, index, notebooks, pycharm, scaffold


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lc", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="scaffold a problem directory")
    new.add_argument("number", type=int, help="LeetCode problem number")
    new.add_argument("title", help='problem title, e.g. "Two Sum"')
    new.add_argument("-d", "--difficulty", choices=["easy", "medium", "hard"], default="medium")
    new.add_argument("-t", "--topics", default="", help="comma separated, e.g. array,hash-table")
    new.add_argument("-e", "--entry", default="", help="LeetCode method name, e.g. twoSum")
    new.add_argument("-n", "--notebook", action="store_true", help="also add explain.ipynb")
    new.add_argument(
        "--no-run-config", action="store_true", help="skip the PyCharm run configuration"
    )

    bm = sub.add_parser("bench", help="time every solution of a problem")
    bm.add_argument("problem", help="number, slug or directory")
    bm.add_argument("-r", "--repeat", type=int, default=1000, help="runs per case (default 1000)")

    sub.add_parser("index", help="regenerate the progress table in README.md")
    sub.add_parser("pycharm", help="regenerate PyCharm run configurations for every problem")

    hook = sub.add_parser("hooks", help="enable the repo's git hooks (.githooks/)")
    hook.add_argument("--uninstall", action="store_true", help="stop using them")

    nb = sub.add_parser("nb", help="strip outputs from notebooks before committing")
    nb.add_argument(
        "--check", action="store_true", help="fail instead of stripping (for hooks and CI)"
    )

    args = parser.parse_args(argv)
    if args.command == "new":
        return scaffold.create(
            number=args.number,
            title=args.title,
            difficulty=args.difficulty,
            topics=[t.strip() for t in args.topics.split(",") if t.strip()],
            entry=args.entry,
            notebook=args.notebook,
            run_config=not args.no_run_config,
        )
    if args.command == "bench":
        return bench.run(args.problem, repeat=args.repeat)
    if args.command == "pycharm":
        return pycharm.sync()
    if args.command == "nb":
        return notebooks.run(check=args.check)
    if args.command == "hooks":
        return hooks.run(uninstall=args.uninstall)
    return index.rebuild()


if __name__ == "__main__":
    sys.exit(main())
