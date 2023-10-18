def init_plugins(settings):
    """Load plugins and call register()."""

    logger = logging.getLogger(__name__)
    logger.debug('Plugin paths: %s', settings['plugin_paths'])

    for path in settings['plugin_paths']:
        sys.path.insert(0, path)

    for plugin in settings['plugins']:
        try:
            if isinstance(plugin, str):
                mod = importlib.import_module(plugin)
                mod.register(settings)
            else:
                plugin.register(settings)
            logger.debug('Registered plugin %s', plugin)
        except Exception as e:
            logger.error('Failed to load plugin %s: %r', plugin, e)

    for path in settings['plugin_paths']:
        sys.path.remove(path)