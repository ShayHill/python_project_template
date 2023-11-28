

# Create a Python venv at ./venv if it doesn't exist
if (!(Test-Path -PathType container "venv"))
{
    py -3.11 -m venv venv
    .\venv\Scripts\python.exe -m pip install --upgrade pip
}

# Read pyproject.toml to create a requirements.txt and dev-requirements.txt
# Use these to update your Python venv at ./venv

.\venv\Scripts\pip install pip-tools
.\venv\Scripts\pip-compile -o requirements.txt pyproject.toml --upgrade --strip-extras
.\venv\Scripts\pip-compile --extra=dev -o dev-requirements.txt pyproject.toml --upgrade --strip-extras
.\venv\Scripts\pip-sync --python-executable .\venv\Scripts\python.exe requirements.txt dev-requirements.txt
.\venv\Scripts\pip install -e .
