import sys

import swmmreport
status = swmmreport.test(*sys.argv[1:])
sys.exit(status)