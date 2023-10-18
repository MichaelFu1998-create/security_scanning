def _load_plugins():
    """
    Locate all setuptools entry points by the name 'keyring backends'
    and initialize them.
    Any third-party library may register an entry point by adding the
    following to their setup.py::

        entry_points = {
            'keyring.backends': [
                'plugin_name = mylib.mymodule:initialize_func',
            ],
        },

    `plugin_name` can be anything, and is only used to display the name
    of the plugin at initialization time.

    `initialize_func` is optional, but will be invoked if callable.
    """
    group = 'keyring.backends'
    entry_points = entrypoints.get_group_all(group=group)
    for ep in entry_points:
        try:
            log.info('Loading %s', ep.name)
            init_func = ep.load()
            if callable(init_func):
                init_func()
        except Exception:
            log.exception("Error initializing plugin %s." % ep)