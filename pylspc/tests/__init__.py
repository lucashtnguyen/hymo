import pytest
from pkg_resources import resource_filename

import pylspc

def test(*args):
    options = [resource_filename('pylspc', 'tests')]
    options.extend(list(args))
    return pytest.main(options)