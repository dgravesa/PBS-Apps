# Daniel Graves

import sys
import os
import json
import apps_util as util

usage = 'usage: apps submit [app_name] [--no-prompt]'
app_name = None
no_prompt = False

i = 1
argc = len(sys.argv)
#while i < argc:
#    if sys.argv[i] == '--no-prompt':
#        no_prompt = True
#    elif sys.argv[i] == '--help' or app_name is not None:
#        print(usage)
#        sys.exit(1)
#    else:
#        app_name = sys.argv[i]
#    i += 1

print_app_usage = False
app_args = []
while i < argc:
    if sys.argv[i] == '--no-prompt':
        no_prompt = True
    elif app_name is None:
        if sys.argv[i] == '--help':
            print(usage)
            sys.exit(1)
        else:
            app_name = sys.argv[i]
    elif app_name is not None:
        if sys.argv[i] == '--help':
            print_app_usage = True
        else:
            app_args.append(sys.argv[i])
    i += 1

app_names = util.get_apps_list()

if len(app_names) == 0:
    util.warn('No apps found in directory: ' + util.apps_dir)
    sys.exit(1)

if not no_prompt and app_name is None:
    util.info()
    util.info('This is the job submission utility')
    util.info('Follow the prompts to submit your job')
    util.info()
    util.info('Available apps:')
    print(*app_names, sep = '\t')
    util.info()

# get application
if app_name is not None:
    if app_name not in app_names:
        util.warn('No app named \'' + app_name +  '\'')
        sys.exit(1)
else:
    app_name_check = False
    while not app_name_check:
        app_name = util.prompt('Enter app name: ')
        if app_name in app_names: app_name_check = True
        else: util.warn('No app named \'' + app_name + '\'')

# get prompts list
app_dir = util.apps_dir + '/' + app_name
with open(app_dir + '/prompts.json', 'r') as infile:
    prompts = json.load(infile)

no_prompts = set()
# avoid all prompts
if no_prompt:
    no_prompts.update(prompts)

# check command line arguments for app
#cl_prompts = ['--' + prompt.lower().replace('_', '-') for prompt in prompts]
cl_prompts = {}
for prompt in prompts:
    cl_prompt = '--' + prompt.lower().replace('_', '-')
    cl_prompts[cl_prompt] = prompt
if print_app_usage:
    print('usage: apps submit ' + app_name + ' ', end = '')
    max_print = 2
    i = 0
    for cl_prompt in cl_prompts:
        if i >= max_print:
            print('...')
            break
        print('[' + cl_prompt + ' ' + cl_prompts[cl_prompt] + '] ', end = '')
        i += 1
    print()
    print('command line arguments:')
    print()
    for cl_prompt in cl_prompts:
        print('  ' + cl_prompt)
    print()
    sys.exit(1)
else:
    # TODO this is an easy solution
    # consider modifying so that prompt does not occur if specified on command line
    i = 0
    argc = len(app_args)
    while i < argc:
        arg = app_args[i]
        if arg in cl_prompts:
            # get next argument as value
            i += 1
            if i == argc:
                util.fail('error: no value specifed for argument \'' + arg + '\'')
                sys.exit(1)
            # place into environment
            os.environ[cl_prompts[arg]] = app_args[i]
            # do not prompt user if provided on command line
            no_prompts.add(cl_prompts[arg])
        i += 1

# get prompts from user
for prompt in prompts:
    
    # get default prompt from environment
    try: default = os.environ[prompt]

    # get default prompt from rule
    except KeyError: default = util.sh(app_dir + '/' + prompt + '.sh')

    # place default into environment
    #if no_prompt:
    if prompt in no_prompts:
        os.environ[prompt] = default

    else:
        # get prompt from user
        if default != '':
            result = util.prompt('Enter ' + prompt + ' (' + default + '): ')
            if result == '': result = default
        else:
            result = util.prompt('Enter ' + prompt + ': ')

        # place value into environment
        os.environ[prompt] = result

# create PBS script
util.info('Writing output PBS script \'submit.pbs\'...')
text = util.get_file_text(app_dir + '/template.pbs')
for arg in prompts:
    text = text.replace('!' + arg, os.environ[arg])
with open('submit.pbs', 'w') as outfile:
    outfile.write(text)

# submit job
if not no_prompt:
    response = util.prompt('Would you like to submit your job now? [Y/(n)] ')
    if response == 'Y' or response == 'y':
        print('Submitting job... ', end = '')
        print(util.sh('submit-job'))
    else:
        util.info('To submit your job, run `qsub submit.pbs`')
else:
    print('Submitting job... ', end = '')
    print(util.sh('submit-job'))

