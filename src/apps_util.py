# Daniel Graves

import os
import subprocess

apps_root = os.environ['APPS_ROOT']
apps_dir = os.environ['APPS_DIR']

style = {
    'default': '\033[0m',
    'success': '\033[92m',
    'prompt': '\033[95m',
    'info': '\033[94m',
    'warn': '\033[93m',
    'fail': '\033[91m'
}

def success(text = ''):
    print(style['success'] + text + style['default'])

def info(text = ''):
    print(style['info'] + text + style['default'])

def warn(text = ''):
    print(style['warn'] + text + style['default'])

def fail(text = ''):
    print(style['fail'] + text + style['default'])

def prompt(text = ''):
    return input(style['prompt'] + text + style['default'])

def warn_prompt(text = ''):
    return input(style['warn'] + text + style['default'])

def get_file_text(file_name):
    with open(file_name, 'r') as input_file:
        return input_file.read()

def get_variables(text, char):
    length = len(text)
    args = []

    # parse text string
    pos = text.find(char)
    while pos >= 0:
        # get variable name
        end = pos + 1
        while end < length and (text[end].isalnum() or text[end] == '_'):
            end += 1
        arg = text[pos + 1:end]

        # add argument to list
        if arg != '' and arg not in args:
            args.append(arg)

        # get next argument instance
        pos = text.find(char, end)

    return args

def get_apps_list():
    return os.listdir(apps_dir)

def sh(script):
    result = subprocess.run(['sh', script], stdout = subprocess.PIPE)
    return result.stdout.decode('UTF-8').rstrip()

