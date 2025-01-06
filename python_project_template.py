"""Lay out an empty Python project.

:author: Shay Hill
:created: 2023-10-05

Run this script from any directory. There are two congifuration variables at the top
of the file: _MY_PROJECTS_DIR and _SNIPPETS_DIR. The resulting file structure will be:

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

import sys
import subprocess
from pathlib import Path
import datetime
import re

# ===============================================================================
#   Configuration
# ===============================================================================

# The parent directory of your Python project root, not the root itself. The
_MY_PROJECTS_DIR = Path.home() / "PythonProjects"

# A directory containing your UltiSnips snippets.
_SNIPPETS_DIR = Path.home() / "vimfiles" / "UltiSnips"


# ===============================================================================
#   Query user for project details
# ===============================================================================

project_name = input("Project name: ")
project_description = input("Project description: ")
python_min_version = input("Minimum Python version (only the n in 3.n): ")
python_max_version = input("Maximum Python version (blank to use current): ")

if python_max_version:
    # assume constrained to a range
    requires_python = f">=3.{python_min_version},<3.{int(python_max_version) + 1}"
else:
    # assume current version is ok
    requires_python = f">=3.{python_min_version}"
    python_max_version = sys.version_info.minor


# ===============================================================================
#   Module-wide variables inferred from configuration and project details
# ===============================================================================

project_root = _MY_PROJECTS_DIR / project_name
creation_date = datetime.datetime.now().strftime("%Y-%m-%d")
init_text_template = f'''"""{{}}

:author: ShayHill
:created: {creation_date}
"""'''


def _select_snippet(
    snippet_file: Path, snippet_trigger: str, subs: dict[str, str] | None = None
) -> str:
    pattern = re.compile(rf"snippet {snippet_trigger}(.*?)endsnippet", re.DOTALL)
    with open(snippet_file) as f:
        match = re.search(pattern, f.read())
    if not match:
        raise ValueError(f"Snippet {snippet_trigger} not found in {snippet_file}")
    match_str = "\n".join(match.group(1).split("\n")[1:])
    for k, v in (subs or {}).items():
        match_str = re.sub(k, v, match_str)
    return match_str


def _write_pyproject_toml():
    toml_snippets = _SNIPPETS_DIR / "toml.snippets"
    pyproject = _select_snippet(
        toml_snippets,
        "pyproject",
        {
            r"\$1": project_name,
            r"\$2": project_description,
            r"\$3": requires_python,
            r"\$4": "",
            r"\$5": '"commitizen", "pre-commit", "pytest", "tox"',
        },
    )
    commitizen = _select_snippet(_SNIPPETS_DIR / "toml.snippets", "cz")
    pyright = _select_snippet(
        toml_snippets, "pyright", {r"\$1": python_min_version, r"\$2": ""}
    )
    isort = _select_snippet(_SNIPPETS_DIR / "toml.snippets", "isort")

    with (project_root / "pyproject.toml").open("w") as f:
        _ = f.write("\n\n".join([pyproject, commitizen, isort, pyright]))


def _write_pre_commit_config():
    yaml_snippets = _SNIPPETS_DIR / "yaml.snippets"
    subs = {r"\$1": str(python_min_version), r"\$2": str(python_max_version)}
    with (project_root / ".pre-commit-config.yaml").open("w") as f:
        _ = f.write(_select_snippet(yaml_snippets, "pre-commit-config", subs))


def _write_tox_ini():
    min_ver = int(python_min_version)
    max_ver = int(python_max_version)
    versions = [f"3{n}" for n in range(min_ver, max_ver + 1)]
    tox_ini_text = [
        "[tox]",
        f"envlist = py{{{','.join(versions[::-1])}}}",
        "",
        "[testenv]",
        "deps = pytest",
        "commands = pytest",
    ]
    with (project_root / "tox.ini").open("w") as f:
        _ = f.write("\n".join(tox_ini_text))


def _write_vimspector_json():
    json_snippets = _SNIPPETS_DIR / "json.snippets"
    with (project_root / ".vimspector.json").open("w") as f:
        _ = f.write(
            _select_snippet(json_snippets, "vimspector", {r"\$1": project_name})
        )


def _write_project_vimrc():
    """`set exrc` in your global vimrc to auto. source a project-specific vimrc."""
    vim_snippets = _SNIPPETS_DIR / "vim.snippets"
    with (project_root / ".vimrc").open("w") as f:
        _ = f.write(_select_snippet(vim_snippets, "local", {r"\$1": project_name}))


def _write_venv_update_script():
    """Create a PowerShell script to sync the venv with pyproject.toml."""
    ps1_snippets = _SNIPPETS_DIR / "ps1.snippets"
    venv_version = f"3.{python_max_version}"
    with (project_root / "Update-PythonVenv.ps1").open("w") as f:
        _ = f.write(
            _select_snippet(ps1_snippets, "update_venv", {r"\$1": venv_version})
        )


def _write_conftest():
    python_snippets = _SNIPPETS_DIR / "python.snippets"
    with (project_root / "tests" / "conftest.py").open("w") as f:
        _ = f.write(_select_snippet(python_snippets, "conftest"))


def _write_gitignore():
    with (project_root / ".gitignore").open("w") as f:
        _ = f.write("Update-PythonVenv.ps1")


def _initialize_git():
    _ = subprocess.run(["git", "init"], cwd=project_root)
    _ = subprocess.run(["git", "checkout", "-b", "dev"], cwd=project_root)
    _ = subprocess.run(["git", "add", "README.md"], cwd=project_root)
    _ = subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_root)


def _update_pre_commit():
    # run pre-commit autoupdate
    cmds = [
        f"py -3.{python_max_version} -m venv venv",
        ".\\venv\\Scripts\\python.exe -m pip install --upgrade pip",
        ".\\venv\\Scripts\\python.exe -m pip install pre-commit",
        ".\\venv\\Scripts\\pre-commit.exe autoupdate",
        ".\\venv\\Scripts\\pre-commit.exe run -a",
    ]
    for cmd in cmds:
        _ = subprocess.run(cmd.split(" "), cwd=project_root, shell=True)


def build_project():
    """Create directories and ini files."""
    src_dir = project_root / "src" / project_name
    test_dir = project_root / "tests"
    src_dir.mkdir(parents=True)
    test_dir.mkdir(parents=True)
    (src_dir / "py.typed").touch()
    _ = (src_dir / "__init__.py").write_text(
        init_text_template.format("Import functions into the package namespace.")
    )
    (test_dir / "__init__.py").touch()
    _ = (project_root / "README.md").write_text(
        "# " + str(project_name) + "\n\n" + project_description + "\n"
    )

    _write_pyproject_toml()
    _write_pre_commit_config()
    _write_tox_ini()
    _write_vimspector_json()
    _write_gitignore()
    _write_venv_update_script()
    _write_conftest()
    _write_project_vimrc()
    _initialize_git()
    _update_pre_commit()


if __name__ == "__main__":
    build_project()
