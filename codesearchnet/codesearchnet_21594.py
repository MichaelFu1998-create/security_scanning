def get_plugin_instance(plugin_class, *args, **kwargs):
    """Returns an instance of a fully initialized plugin class

    Every plugin class is kept in a plugin cache, effectively making
    every plugin into a singleton object.

    When a plugin has a yaz.dependency decorator, it will be called
    as well, before the instance is returned.
    """
    assert issubclass(plugin_class, BasePlugin), type(plugin_class)

    global _yaz_plugin_instance_cache

    qualname = plugin_class.__qualname__
    if not qualname in _yaz_plugin_instance_cache:
        plugin_class = get_plugin_list()[qualname]
        _yaz_plugin_instance_cache[qualname] = plugin = plugin_class(*args, **kwargs)

        # find any yaz.dependency decorators, and call them when necessary
        funcs = [func
                 for _, func
                 in inspect.getmembers(plugin)
                 if inspect.ismethod(func) and hasattr(func, "yaz_dependency_config")]

        for func in funcs:
            signature = inspect.signature(func)
            assert all(parameter.kind is parameter.POSITIONAL_OR_KEYWORD and issubclass(parameter.annotation, BasePlugin) for parameter in signature.parameters.values()), "All parameters for {} must type hint to a BasePlugin".format(func)
            func(*[get_plugin_instance(parameter.annotation)
                   for parameter
                   in signature.parameters.values()])

    return _yaz_plugin_instance_cache[qualname]