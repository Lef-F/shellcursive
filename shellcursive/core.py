# TODO: Replace GitPython with a more generic shell execution
from git.cmd import Git
from git import GitCommandError
from pathlib import Path
from dataclasses import dataclass, field
from rich.progress import track


@dataclass
class Results:
    """Object to store git paths to traverse and command execution status."""

    git_paths: list[str | Path]  # The paths to crawl
    failures: dict[str, str] = field(
        default_factory=dict
    )  # The paths where the commands failed, {"/path1": "error message"}
    successes: list[str] = field(
        default_factory=list
    )  # The paths where the commands succeeded

    @property
    def num_of_failures(self) -> int:
        return len(self.failures)

    @property
    def num_of_successes(self) -> int:
        return len(self.successes)

    @property
    def num_of_paths(self) -> int:
        return len(self.git_paths)


def path_crawler(path: Path | str, pattern: str) -> list[Path]:
    p = Path(path)
    git_paths = list()
    for git_path in p.glob(pattern=pattern):
        git_paths.append(git_path.parent)
    return git_paths


def execute(command: list[str], git_paths: list[Path | str]) -> Results:
    results = Results(git_paths=git_paths)
    for path in track(results.git_paths):
        resolved_path = path.resolve()
        cmd = Git(working_dir=path)
        try:
            cmd.execute(command=command)
            results.successes.append(str(resolved_path))
            print(f"SUCCESS: {resolved_path}")
        except GitCommandError as e:
            print(f"FAILED: {resolved_path}")
            results.failures.update({str(resolved_path): e.stderr})
    return results
