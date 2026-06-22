"""Retrieve the latest released version of Python.

:author: Shay Hill
:created: 2026-06-21
"""

import re

import requests

_RELEASE_API = "https://www.python.org/api/v2/downloads/release/"

_RE_VERSION = re.compile(r"Python (\d+)\.(\d+)\.(\d+)$")


def get_latest_python_version() -> tuple[int, int, int]:
    """Return the latest stable Python version, e.g. "3.13.5"."""
    response = requests.get(_RELEASE_API, timeout=30)
    response.raise_for_status()
    releases = (x for x in response.json() if not x.get("pre_release"))
    versions = filter(None, (_RE_VERSION.match(r.get("name", "")) for r in releases))
    try:
        maj, min_, patch = max(tuple(map(int, v.groups())) for v in versions)
        return maj, min_, patch
    except ValueError:
        msg = "No stable Python release found."
        raise RuntimeError(msg)
