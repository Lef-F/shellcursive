from core import path_crawler, execute
from argparse import ArgumentParser
from pathlib import Path
from rich.console import Console
from rich.table import Column, Table

parser = ArgumentParser(
    description="Execute commands in every git repository under the given path."
)

parser.add_argument("path", help="The path to search for available git repos.")
parser.add_argument(
    "command",
    help="The command to recursively execute in all available git repos.",
    nargs="*",
)
parser.add_argument(
    "--command-file",
    help="A file with the commands to execute, newline separated.",
    required=False,
)
parser.add_argument(
    "--pattern",
    help="The pattern to match files or folders in the given path. "
    + "The commands will be executed inside the matching folders. "
    + "(default: %(default)s)",
    default="**/.git/",
    required=False,
)

args = parser.parse_args()


def main() -> None:
    if args.command_file:
        raise NotImplementedError()

    resolved_path = Path(args.path).resolve()
    if not resolved_path.exists():
        raise ValueError(f"The path provided does not exist: {resolved_path}")

    git_repos_paths = [
        path.resolve() for path in path_crawler(args.path, pattern=args.pattern)
    ]

    tbl_paths = Table(
        Column("Path"),
        title=f"{len(git_repos_paths)} Repositories Found in path {resolved_path}",
    )

    _ = [tbl_paths.add_row(str(row)) for row in git_repos_paths]

    console = Console()
    console.print(tbl_paths)

    results = execute(args.command, git_repos_paths)
    tbl_results = Table(
        Column("Path"), Column("Outcome"), Column("Error Message"), title="Results"
    )

    _ = [
        tbl_results.add_row(success, "[green]:heavy_check_mark:", None)
        for success in results.successes
    ]
    tbl_results.add_section()
    _ = [
        tbl_results.add_row(path, "[bold red]FAILED", failure, end_section=True)
        for path, failure in results.failures.items()
    ]

    console.print(tbl_results)

    print(f"Total paths: {results.num_of_paths}")
    print(f"Failed paths: {results.num_of_failures}")
    print(f"Success paths: {results.num_of_successes}")
    print(
        f"Success ratio: {100*(results.num_of_successes / results.num_of_paths):.1f}%"
    )


if __name__ == "__main__":
    main()
    exit(0)
