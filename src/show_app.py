# Daniel Graves

import sys
import apps_util as util
import json

usage = 'usage: apps show app_name [--arguments]'
app_name = None
show_arguments = False

# parse command line arguments
i = 1
argc = len(sys.argv)
while i < argc:
    if sys.argv[i] == '--arguments':
        show_arguments = True
    elif sys.argv[i] == '--help' or app_name is not None:
        print(usage)
        sys.exit(1)
    else:
        app_name = sys.argv[i]
    i += 1
if app_name is None:
    print(usage)
    sys.exit(1)

# app not found
if app_name not in util.get_apps_list():
    util.warn('No app named \'' + app_name + '\'')
    sys.exit(1)

if show_arguments:
    with open(util.apps_dir + '/' + app_name + '/prompts.json', 'r') as prompts_file:
        prompts = json.load(prompts_file)
    for prompt in prompts:
        print(prompt)
else:
    text = util.get_file_text(util.apps_dir + '/' + app_name + '/template.pbs')
    print()
    print(text)
    print()

