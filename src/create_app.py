# Daniel Graves

import os
import sys
import shutil
import json
import apps_util as util

usage = 'usage: apps create [app_name] [-t pbs_template]'
app_name = None
input_file = None

# parse command line arguments
i = 1
argc = len(sys.argv)
while i < argc:
    if sys.argv[i] == '-t':
        i += 1
        if i == argc:
            print(usage)
            sys.exit(1)
        else:
            input_file = sys.argv[i]
    elif sys.argv[i] == '-h' or sys.argv[i] == '--help' or app_name is not None:
        print(usage)
        sys.exit(1)
    else:
        app_name = sys.argv[i]
    i += 1

util.info()
util.info('This is the app creation utility.')
util.info('Follow the prompts to create your application.')
util.info()

## get application name
#app_name_check = False
#while not app_name_check:
#    app_name = util.prompt('Enter app name: ')
#    if app_name in util.get_apps_list():
#        response = util.warn_prompt('App \'' + app_name + '\' already exists. Overwrite? [Y/(n)] ')
#        if response == 'Y' or response == 'y': app_name_check = True
#    else: app_name_check = True

## get application name
#while app_name is None:
#    app_name = util.prompt('Enter app name: ')
#    if app_name in util.get_apps_list():
#        response = util.warn_prompt('App \'' + app_name + '\' already exists. Overwrite? [Y/(n)] ')
#        if response != 'Y' and response != 'y': app_name = None
#        else: shutil.rmtree(util.apps_dir + '/' + app_name)

# get application name and check for existing application
if app_name is None: app_name = util.prompt('Enter app name: ')
app_name_check = app_name not in util.get_apps_list()
while not app_name_check:
    response = util.warn_prompt('App \'' + app_name + '\' already exists. Overwrite? [Y/(n)] ')
    if response == 'Y' or response == 'y':
        app_name_check = True
        shutil.rmtree(util.apps_dir + '/' + app_name)
    else:
        app_name = util.prompt('Enter app name: ')
        app_name_check = app_name not in util.get_apps_list()

# get pbs template file name
if input_file is None:
    input_file = util.prompt('Enter PBS template file: ')
text = util.get_file_text(input_file)
pbs_args = util.get_variables(text, '!')

# print creation dialog
util.info()
util.info('Detected PBS arguments:')
for arg in pbs_args:
    util.info(arg)
util.info()
util.info('For each PBS arguments, do one of the following:')
util.info('- leave blank to require user input on job submission')
util.info('- * specify a default value (users will still be prompted on job submission) *')
util.info('- * specify a rule surrounded by `` marks (users will still be prompted on job submission) *')
util.info('- type "VOID" to discard the argument')
util.info()
util.info('* default values or rules may contain environment variables or other arguments written as environment variables *')
util.info()

# prompt user for argument rules
arg_rules = {}
for arg in pbs_args:
    rule = util.prompt('Enter ' + arg + ': ')
    #arg_rules[arg] = util.prompt('Enter ' + arg + ': ')
    if rule != "VOID": arg_rules[arg] = rule

# reconstruct pbs_args from non-discarded arguments
pbs_args = []
for arg in arg_rules:
    pbs_args.append(arg)

# initialize dependency graph
dep_graph = {}
for arg in pbs_args:
    dep_graph[arg] = { 'dependencies': [], 'dependents': [] }

# create dependency graph from rules
for arg in pbs_args:
    
    # get dependencies
    vars = util.get_variables(arg_rules[arg], '$')
    dep_graph[arg]['dependencies'] = list(set(pbs_args) & set(vars))
    
    # set as dependent in dependencies
    for dep in dep_graph[arg]['dependencies']:
        dep_graph[dep]['dependents'].append(arg)

# create prompt order and check for cyclic dependencies
prompt_order = []
while len(dep_graph) > 0:
    update = False

    # find key with satisfied dependencies
    for key in dep_graph:
        if len(dep_graph[key]['dependencies']) == 0:
            update = True
            break

    # cycle detected
    if not update:
        util.error('Error: cyclic dependency detected on argument rules')
        sys.exit(1)

    # add prompt to order
    prompt_order.append(key)

    # remove dependency from dependents
    for dependent in dep_graph[key]['dependents']:
        dep_graph[dependent]['dependencies'].remove(key)

    # remove node from dependency graph
    dep_graph.pop(key)

# create application
app_dir = util.apps_dir + '/' + app_name
util.info()
util.info('Saving application to \'' + app_dir + '\'...')
os.mkdir(app_dir)

# copy PBS script into app directory
shutil.copy(input_file, app_dir + '/template.pbs')

# create rule scripts
for arg in pbs_args:
    with open(app_dir + '/' + arg + '.sh', 'w') as script:
        script.write('echo \"' + arg_rules[arg] + '\"\n')

# save prompt order to JSON
with open(app_dir + '/prompts.json', 'w') as outfile:
    json.dump(prompt_order, outfile)

util.success('Successfully created application \'' + app_name + '\'')

