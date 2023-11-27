# python_project_template

my standard Python project template

I use a script to create this, there are too many names and versions to update by hand. The script `python_project_update.py` is here, along with `Update-PythonVenv.ps1`, which I usually would not commit.

The script is the only thing that matters, because there is too much noise in a Python project to just clone one and use it. The rest is here for conversation's sake. This is the canonical version of my Python project template script. The canonical versions of most of the files are in my `~\vimfiles\Ultisnips` dir.

In addition to creating files, the script

* creates and activates a Python venv
* creates pre-commit environment
* initializes git
* makes 0th commit with just a mostly empty `README.md`
* creates and checks out dev branch

The script does not query for dependencies. To add dependencies

* edit `pyproject.toml`
* deactivate the venv
* `py Update-PythonVenv.ps1` (this will require pip-tools in your system Python)

The final structure is

```
MY_PROJECTS_DIR
└── project_name
    ├── src
    │   └── project_name
    │       ├── __init__.py
    │       └── py.typed
    ├── tests
    │   ├── __init__.py
    │   └── conftest.py
    ├── .git
    ├── .gitignore
    ├── .pre-commit-config.yaml
    ├── .vimrc
    ├── .vimspector.json
    ├── README.md
    ├── Update-PythonVenv.ps1
    ├── pyproject.toml
    └── tox.ini
```
