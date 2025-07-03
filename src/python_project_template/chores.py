"""Small chores that are run at the beginning of a project.

:author: Shay Hill
:created: 2025-07-02
"""

import subprocess

from python_project_template import paths
from python_project_template.user_input import UserInput


def initialize_git(user: UserInput) -> None:
    """Initialize a git repository andke an initial commit."""

    def git_run(cmd: list[str]) -> None:
        cmd = [paths.GIT, *cmd]
        _ = subprocess.run(cmd, cwd=user.project_root, check=True)

    git_run(["init"])
    git_run(["checkout", "-b", "dev"])
    git_run(["add", "README.md"])
    git_run(["commit", "-m", "Initial commit"])


