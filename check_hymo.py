import sys

import hymo
status = hymo.test(*sys.argv[1:])
sys.exit(status)