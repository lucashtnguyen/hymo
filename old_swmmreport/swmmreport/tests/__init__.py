import pytest
from pkg_resources import resource_filename

import swmmreport

def test(*args):
    options = [resource_filename('swmmreport', 'tests')]
    options.extend(list(args))
    return pytest.main(options)