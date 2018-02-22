# Daniel Graves
# delete_app.py

import sys
from shutil import rmtree
import apps_util as util

usage = 'usage: apps delete app_name [--no-prompt]'
app_name = None
no_prompt = False

i = 1
argc = len(sys.argv)
while i < argc:
    if sys.argv[i] == '--no-prompt':
        no_prompt = True
    elif sys.argv[i] == '--help' or app_name is not None:
        print(usage)
        sys.exit(1)
    else:
        app_name = sys.argv[i]
    i += 1
if app_name is None:
    print(usage)
    sys.exit(1)

if app_name in util.get_apps_list():
    if not no_prompt:
        response = util.warn_prompt('Are you sure you want to delete the app \'' + app_name + '\'? [Y/(n)] ')
        if response != 'Y' and response != 'y':
            sys.exit(0)
    rmtree(util.apps_dir + '/' + app_name)
    util.success('Successfully deleted app \'' + app_name + '\'')
else:
    util.warn('No app named \'' + app_name + '\'')
    sys.exit(1)

