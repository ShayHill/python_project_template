

# Create a Python venv at ./venv if it doesn't exist

if (!(Test-Path -PathType container "source"))
{
	py -m venv venv
}

# Read pyproject.toml to create a requirements.txt and dev-requirements.txt
# Use these to update your Python venv at ./venv

py -m pip-compile -o requirements.txt pyproject.toml --upgrade --strip-extras
py -m pip-compile --extra=dev -o dev-requirements.txt pyproject.toml --upgrade --strip-extras
venv\Scripts\activate
py -m pip-sync --python-executable .\venv\Scripts\python.exe requirements.txt dev-requirements.txt
python -m pip install -e .