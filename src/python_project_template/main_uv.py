"""Create an empty project using the `uv` package.

Run this script from any directory. The resulting file structure will be:

MY_PROJECTS_DIR/
└── project_name/
    ├── src/
    │   └── project_name/
    │       ├── __init__.py
    │       └── py.typed
    ├── tests/
    │   ├── __init__.py
    │   └── conftest.py
    ├── .git
    ├── .gitignore
    ├── .pre-commit-config.yaml
    ├── .vimrc
    ├── .vimspector.json
    ├── README.md
    ├── Update-PythonVenv.ps1
    └── pyproject.toml

After running this script, the venv will be created. To add more dependencies

uv add <dependency>

to update:
uv lock --upgrade
uv sync

:author: Shay Hill
:created: 2025-07-02
"""

from __future__ import annotations

import subprocess

from python_project_template import chores, paths, project_files
from python_project_template.project_files import select_snippet
from python_project_template.user_input import UserInput


def _init_project(user: UserInput) -> None:
    """Initialize a new project using the `uv` package."""
    # fmt: off
    init_cmd = [
        "uv", "init", "--lib",
        user.project_name,
        "--description", user.project_description,
        "--python", f"3.{user.python_min_version}",
    ]
    # fmt: on
    _ = subprocess.run(init_cmd, cwd=paths.MY_PROJECTS_DIR, check=True)
    for dep in user.deps:
        dep_cmd = ["uv", "add", dep]
        _ = subprocess.run(dep_cmd, cwd=user.project_root, check=True)

    for dep in user.dev_deps:
        dep_cmd = ["uv", "add", dep, "--dev"]
        _ = subprocess.run(dep_cmd, cwd=user.project_root, check=True)


def _add_tool_config_to_pyproject(user: UserInput) -> None:
    """Add the tool configurations to the pyproject.toml file."""
    toml_snippets = paths.SNIPPETS_DIR / "toml.snippets"

    commitizen = select_snippet(paths.SNIPPETS_DIR / "toml.snippets", "cz")
    pyright = select_snippet(
        toml_snippets, "pyright", {r"\$1": user.python_min_version, r"\$2": ""}
    ).replace('venv = "./venv"', 'venv = "./.venv"')
    isort = select_snippet(paths.SNIPPETS_DIR / "toml.snippets", "isort")
    tox_envs = ",".join(
        [
            f"3{n}"
            for n in range(
                int(user.python_min_version), int(user.python_max_version) + 1
            )
        ]
    )
    tox = select_snippet(
        paths.SNIPPETS_DIR / "toml.snippets", "tox", {r"\$1": tox_envs}
    )

    with (user.project_root / "pyproject.toml").open("a") as f:
        _ = f.write("\n\n")
        _ = f.write("\n\n".join([commitizen, isort, tox, pyright]))


def _add_license_to_pyproject(user: UserInput) -> None:
    """Add the license information to the pyproject.toml file."""
    pyproject = user.project_root / "pyproject.toml"
    with pyproject.open() as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'readme = "README.md"' in line:
            lines.insert(i + 1, 'license = "MIT"\n')
            break
    else:
        msg = "Could not find the readme line in pyproject.toml"
        raise ValueError(msg)
    with pyproject.open("w") as f:
        f.writelines(lines)


def _update_pre_commit(user: UserInput) -> None:
    """Run pre-commit autoupdate and run all hooks."""
    scripts = user.project_root / ".venv" / "Scripts"
    pre_commit = scripts / "pre-commit.exe"

    cmds = [
        f"{pre_commit} autoupdate",
        f"{pre_commit} run -a",
    ]
    for cmd in cmds:
        _ = subprocess.run(cmd.split(" "), cwd=user.project_root, check=True)


def build_project() -> None:
    """Create directories and ini files."""
    user = UserInput()
    _init_project(user)
    _add_tool_config_to_pyproject(user)
    _add_license_to_pyproject(user)

    project_files.write_py_typed(user)
    project_files.write_src_init(user)
    project_files.write_test_init(user)
    project_files.write_readme(user)
    project_files.write_pre_commit_config(user)
    project_files.write_vimspector_json(user)
    project_files.write_conftest(user)
    project_files.write_project_vimrc(user)

    chores.initialize_git(user)
    _update_pre_commit(user)


if __name__ == "__main__":
    build_project()
