from importlib.resources import files

import hymo
from .utils import data_path

def test(*args):
    import pytest
    options = [str(files("hymo") / "tests")]
    options.extend(list(args))
    return pytest.main(options)
