import pathlib
import subprocess
from collections.abc import Generator

import pytest


class GitRepo:
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path

    def run(
        self, *args: str, input: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            list(args),
            capture_output=True,
            text=True,
            cwd=self.path,
            input=input,
        )

    def git(self, *args: str) -> str:
        r = self.run("git", *args)
        assert r.returncode == 0, f"git {' '.join(args)} failed: {r.stderr}"
        return r.stdout

    def write_file(self, name: str, content: str) -> str:
        filepath = self.path / name
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)
        return str(filepath)


@pytest.fixture
def git_repo(tmp_path: pathlib.Path) -> Generator[GitRepo]:
    repo = GitRepo(tmp_path)
    repo.git("init")
    repo.git("config", "user.email", "test@test.com")
    repo.git("config", "user.name", "Test")
    yield repo
