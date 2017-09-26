import pytest
from pkg_resources import resource_filename

import hymo

def test(*args):
    options = [resource_filename('hymo', 'tests')]
    options.extend(list(args))
    return pytest.main(options)