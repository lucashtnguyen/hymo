import sys

import lspcreport
status = lspcreport.test(*sys.argv[1:])
sys.exit(status)