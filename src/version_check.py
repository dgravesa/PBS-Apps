# Daniel Graves
# verison_check.py

import sys

if sys.version_info[0:2] < (3, 5):
    sys.stderr.write('Error: Python version 3.5 or higher required\n')
    sys.exit(1)

