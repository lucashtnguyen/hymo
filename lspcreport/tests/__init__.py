import pytest
from pkg_resources import resource_filename

import lspcreport

def test(*args):
    options = [resource_filename('lspcreport', 'tests')]
    options.extend(list(args))
    return pytest.main(options)