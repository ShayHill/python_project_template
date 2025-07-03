"""Lay out an empty Python project.

:author: Shay Hill
:created: 2023-10-05

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

After running this script, the venv will be activated. To add more dependencies

* edit pyproject.toml
* deactivate the venv
* run `Update-PythonVenv.ps1` (this will require pip-tools in your system Python)
"""

from __future__ import annotations

import subprocess

from python_project_template import chores, paths, project_files
from python_project_template.project_files import format_dependencies, select_snippet
from python_project_template.user_input import UserInput


def _write_pyproject_toml(user: UserInput) -> None:
    """Create a pyproject.toml file for a setuptools project."""
    toml_snippets = paths.SNIPPETS_DIR / "toml.snippets"
    pyproject = select_snippet(
        toml_snippets,
        "pyproject",
        {
            r"\$1": user.project_name,
            r"\$2": user.project_description,
            r"\$3": user.requires_python,
            r"\$4": format_dependencies(user.deps),
            r"\$5": format_dependencies(user.dev_deps),
        },
    )
    commitizen = select_snippet(paths.SNIPPETS_DIR / "toml.snippets", "cz")
    pyright = select_snippet(
        toml_snippets, "pyright", {r"\$1": user.python_min_version, r"\$2": ""}
    )
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

    with (user.project_root / "pyproject.toml").open("w") as f:
        _ = f.write("\n\n".join([pyproject, commitizen, isort, tox, pyright]))


def _write_venv_update_script(user: UserInput) -> None:
    """Create a PowerShell script to sync the venv with pyproject.toml."""
    ps1_snippets = paths.SNIPPETS_DIR / "ps1.snippets"
    venv_version = f"3.{user.python_min_version}"
    with (user.project_root / "Update-PythonVenv.ps1").open("w") as f:
        _ = f.write(select_snippet(ps1_snippets, "update_venv", {r"\$1": venv_version}))


def _write_gitignore(user: UserInput) -> None:
    with (user.project_root / ".gitignore").open("w") as f:
        _ = f.write("Update-PythonVenv.ps1")


def _update_pre_commit(user: UserInput) -> None:
    """Run pre-commit autoupdate and run all hooks."""
    update_venv = user.project_root / "Update-PythonVenv.ps1"
    scripts = user.project_root / "venv" / "Scripts"
    python = scripts / "python.exe"
    pre_commit = scripts / "pre-commit.exe"

    cmds = [
        f"powershell -ExecutionPolicy Unrestricted -File {update_venv}",
        f"{python} -m pip install --upgrade pip",
        f"{python} -m pip install pre-commit",
        f"{pre_commit} autoupdate",
        f"{pre_commit} run -a",
    ]
    for cmd in cmds:
        _ = subprocess.run(cmd.split(" "), cwd=user.project_root, check=True)


def build_project() -> None:
    """Create directories and ini files."""
    user = UserInput()
    project_files.write_py_typed(user)
    project_files.write_src_init(user)
    project_files.write_test_init(user)
    project_files.write_readme(user)
    _write_pyproject_toml(user)
    project_files.write_pre_commit_config(user)
    project_files.write_vimspector_json(user)
    _write_gitignore(user)
    project_files.write_conftest(user)
    project_files.write_project_vimrc(user)

    _write_venv_update_script(user)
    chores.initialize_git(user)
    _update_pre_commit(user)


if __name__ == "__main__":
    build_project()
