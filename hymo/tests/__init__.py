import pytest
from pkg_resources import resource_filename

import hymo
from .utils import data_path

def test(*args):
    options = [resource_filename('hymo', 'tests')]
    options.extend(list(args))
    return pytest.main(options)