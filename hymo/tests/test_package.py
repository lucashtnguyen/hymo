import tomllib
from pathlib import Path

import hymo


def test_public_api_exports():
    assert hymo.SWMMReportFile
    assert hymo.SWMMInpFile
    assert hymo.SWMMInterfaceFile
    assert hymo.LSPCResultsFile
    assert hymo.LSPCInpFile
    assert callable(hymo.test)


def test_project_metadata_tracks_modern_test_environment():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    assert pyproject["project"]["requires-python"] == ">=3.11"
    assert "pandas>=3.0.3" in pyproject["project"]["dependencies"]
    assert "pytest" in pyproject["dependency-groups"]["dev"]
