def get_plugin_list():
    """Finds all yaz plugins and returns them in a __qualname__: plugin_class dictionary"""
    global _yaz_plugin_classes

    def get_recursively(cls, plugin_list):
        for plugin in cls.__subclasses__():
            if not (plugin.yaz_is_final() or plugin.__qualname__ in _yaz_plugin_classes):
                plugin_list[plugin.__qualname__].append(plugin)
            get_recursively(plugin, plugin_list)
        return plugin_list

    def include_class(candidate, classes):
        for cls in classes:
            if candidate is cls:
                continue

            if issubclass(cls, candidate):
                return False

        return True

    def get_plugin_type(qualname, plugins):
        classes = sorted(plugins, key=lambda plugin: plugin.yaz_get_ordinal())

        # exclude classes that are implicitly included as parent classes
        classes = [cls for cls in classes if include_class(cls, classes)]
        logger.debug("New plugin class \"%s\" extending %s", qualname, [cls for cls in classes])

        return type(qualname, tuple(classes) + (Final,), {})

    logger.debug("Plugin list: %s" % _yaz_plugin_classes)

    # find all Plugin classes recursively
    plugin_list = get_recursively(BasePlugin, collections.defaultdict(list))

    # combine all classes into their Plugin class (i.e. multiple inherited plugin)
    _yaz_plugin_classes.update((qualname, get_plugin_type(qualname, plugins))
                               for qualname, plugins
                               in plugin_list.items())

    assert isinstance(_yaz_plugin_classes, dict), type(_yaz_plugin_classes)
    assert all(isinstance(qualname, str) for qualname in _yaz_plugin_classes.keys()), "Every key should be a string"
    assert all(issubclass(plugin_class, Final) for plugin_class in _yaz_plugin_classes.values()), "Every value should be a 'Final' plugin"

    return _yaz_plugin_classes