import sys

import pylspc
status = pylspc.test(*sys.argv[1:])
sys.exit(status)