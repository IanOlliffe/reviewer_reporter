from utils import plugins

PLUGIN_NAME = 'Reviewer Reporter Plugin'
DISPLAY_NAME = 'Reviewer Reporter'
DESCRIPTION = 'Reports reviewers.'
AUTHOR = 'Reviewer Reporter'
VERSION = '0.1'
SHORT_NAME = 'reviewer_reporter'
MANAGER_URL = 'reviewer_reporter'
JANEWAY_VERSION = "1.3.8"



class Reviewer_reporterPlugin(plugins.Plugin):
    plugin_name = PLUGIN_NAME
    display_name = DISPLAY_NAME
    description = DESCRIPTION
    author = AUTHOR
    short_name = SHORT_NAME
    manager_url = MANAGER_URL

    version = VERSION
    janeway_version = JANEWAY_VERSION
    


def install():
    Reviewer_reporterPlugin.install()


def hook_registry():
    Reviewer_reporterPlugin.hook_registry()


def register_for_events():
    pass
