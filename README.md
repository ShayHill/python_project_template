# python_project_template

tag 0.2.0 is the last version with setuptools support. This now only creates uv projects.

my standard Python project template

```
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
```

There is too much noise in a Python project to just clone one and use it. This is the canonical version of my Python project template script. The canonical versions of most of the files are in my `~\vimfiles\Ultisnips` dir.

In addition to creating files, the script

* creates a Python venv in `project_root\.venv`
* creates pre-commit environment
* initializes git
* makes 0th commit with just a mostly empty `README.md`
* creates and checks out dev branch
