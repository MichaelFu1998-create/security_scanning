def plugins_show(what=None, name=None, version=None, details=False):
    """
    Show details of available plugins

    Parameters
    ----------
    what: Class of plugins e.g., backend
    name: Name of the plugin e.g., s3
    version: Version of the plugin
    details: Show details be shown?

    """
    global pluginmgr
    return pluginmgr.show(what, name, version, details)