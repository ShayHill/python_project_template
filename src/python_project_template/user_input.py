"""Query user for project details.

:author: Shay Hill
:created: 2025-07-02
"""

import datetime
import sys
from pathlib import Path

from python_project_template import paths

_DEFAULT_DEV_DEPS = ["commitizen", "pre-commit", "pytest", "tox"]


class UserInput:
    """User input for project configuration."""

    def __init__(self) -> None:
        """Initialize the user input with project details."""
        project_name = input("Project name: ")
        self.project_name = project_name or "temp_project"
        self.project_description = input("Project description: ")
        python_min_version = input("Minimum Python version (only the n in 3.n): ")
        self.python_min_version = python_min_version or "10"
        self._python_max_version = input(
            "Maximum Python version (blank to use current): "
        )

        deps_user_input = input("Dependencies (comma-separated): ")
        self.deps = (
            [x.strip() for x in deps_user_input.split(",")] if deps_user_input else []
        )

        dev_deps_user_input = input(
            f"Dev dependencies (comma-separated) default = {_DEFAULT_DEV_DEPS}: "
        )
        self.dev_deps = (
            [x.strip() for x in dev_deps_user_input.split(",")]
            if dev_deps_user_input
            else _DEFAULT_DEV_DEPS
        )
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%d")

    @property
    def project_root(self) -> Path:
        """Return the project root directory."""
        return paths.MY_PROJECTS_DIR / self.project_name

    @property
    def requires_python(self) -> str:
        """Return the requires_python string based on user input."""
        if self._python_max_version:
            # assume constrained to a range
            return (
                f">=3.{self.python_min_version},<3.{int(self._python_max_version) + 1}"
            )
        # assume current version is ok
        return f">=3.{self.python_min_version}"

    @property
    def python_max_version(self) -> str:
        """Return the maximum Python version."""
        return self._python_max_version or str(sys.version_info.minor)

    @property
    def init_text_template(self) -> str:
        """Return the template for the __init__.py file."""
        lines = [
            '"""{{}}',
            "",
            ":author: ShayHill",
            f":created: {self.creation_date}",
            '"""',
        ]
        return "".join(lines)
