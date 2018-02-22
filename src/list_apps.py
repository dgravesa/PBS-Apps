# Daniel Graves

import apps_util as util

apps = util.get_apps_list()

if len(apps) > 0:
    util.info('Available apps:')
    print(*apps, sep = '\t')

else:
    util.warn('No apps found in directory: ' + util.apps_dir)

