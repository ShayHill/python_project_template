"""Format snippets into Python project files.

:author: Shay Hill
:created: 2025-07-02
"""

import re
from pathlib import Path

from python_project_template import paths
from python_project_template.user_input import UserInput


def select_snippet(
    snippet_file: Path, snippet_trigger: str, subs: dict[str, str] | None = None
) -> str:
    """Select a snippet file and fill in the template with substitutions.

    :param snippet_file: Path to the file containing snippets.
    :param snippet_trigger: The trigger for the snippet to select.
    :param subs: Optional dictionary of substitutions to apply to the snippet.
    :return: The formatted snippet as a string.
    """
    pattern = re.compile(rf"snippet {snippet_trigger}(.*?)endsnippet", re.DOTALL)
    with snippet_file.open() as f:
        match = re.search(pattern, f.read())
    if not match:
        msg = f"Snippet {snippet_trigger} not found in {snippet_file}"
        raise ValueError(msg)
    match_str = "\n".join(match.group(1).split("\n")[1:])
    for k, v in (subs or {}).items():
        match_str = re.sub(k, v, match_str)
    return match_str


def format_dependencies(deps_: list[str]) -> str:
    """Format dependencies for pyproject.toml."""
    return ", ".join([f'"{dep}"' for dep in deps_])


def write_pre_commit_config(user: UserInput) -> None:
    """Write a pre-commit configuration file."""
    yaml_snippets = paths.SNIPPETS_DIR / "yaml.snippets"
    subs = {r"\$1": str(user.python_min_version), r"\$2": str(user.python_min_version)}
    with (user.project_root / ".pre-commit-config.yaml").open("w") as f:
        _ = f.write(select_snippet(yaml_snippets, "pre-commit-config", subs))


def write_vimspector_json(user: UserInput) -> None:
    """Write a vimspector configuration file for debugging."""
    json_snippets = paths.SNIPPETS_DIR / "json.snippets"
    with (user.project_root / ".vimspector.json").open("w") as f:
        _ = f.write(
            select_snippet(json_snippets, "vimspector", {r"\$1": user.project_name})
        )


def write_project_vimrc(user: UserInput) -> None:
    """`set exrc` in your global vimrc to auto. source a project-specific vimrc."""
    vim_snippets = paths.SNIPPETS_DIR / "vim.snippets"
    with (user.project_root / ".vimrc").open("w") as f:
        _ = f.write(select_snippet(vim_snippets, "local", {r"\$1": user.project_name}))


def write_conftest(user: UserInput) -> None:
    """Create a conftest.py file for pytest configuration."""
    python_snippets = paths.SNIPPETS_DIR / "python.snippets"
    text = select_snippet(python_snippets, "conftest")
    text = text.replace('`!v strftime("%Y-%m-%d")`', user.creation_date)
    with (user.project_root / "tests" / "conftest.py").open("w") as f:
        _ = f.write(text)


def write_py_typed(user: UserInput) -> None:
    """Create a py.typed file to indicate that the package is typed.

    A uv project should already have an empty `py.typed` file, but call this to
    update the content.
    """
    src_dir = user.project_root / "src" / user.project_name
    src_dir.mkdir(parents=True, exist_ok=True)
    _ = (src_dir / "py.typed").write_text(
        '""" This file is used to indicate to mypy that the package is typed.\n'
        + "\n"
        + "Do not delete this comment, because empty files choke\n"
        + "some cloud drives on sync.\n"
        + '"""'
    )


def write_src_init(user: UserInput) -> None:
    """Create an __init__.py file in the src directory.

    A uv project should already have an `__init__.py` with a test function. Replace
    that function with this.
    """
    src_dir = user.project_root / "src" / user.project_name
    src_dir.mkdir(parents=True, exist_ok=True)
    _ = (src_dir / "__init__.py").write_text(
        user.init_text_template.format("Import functions into the package namespace.")
    )


def write_test_init(user: UserInput) -> None:
    """Create an __init__.py file in the tests directory."""
    test_dir = user.project_root / "tests"
    test_dir.mkdir(parents=True, exist_ok=True)
    _ = (test_dir / "__init__.py").write_text(
        user.init_text_template.format("Mark the 'tests' directory as a package.")
    )


def write_readme(user: UserInput) -> None:
    """Create a simple README.md file in the project root."""
    _ = (user.project_root / "README.md").write_text(
        "# " + str(user.project_name) + "\n\n" + user.project_description + "\n"
    )
