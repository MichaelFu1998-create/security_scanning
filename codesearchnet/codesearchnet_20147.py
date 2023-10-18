def proxy_settings_module(depth=3):
    """Replaces a settings module with a Module proxy to intercept
    an access to settings.

    :param int depth: Frame count to go backward.

    """
    proxies = []

    modules = sys.modules
    module_name = get_frame_locals(depth)['__name__']

    module_real = modules[module_name]

    for name, locals_dict in traverse_local_prefs(depth):

        value = locals_dict[name]

        if isinstance(value, PrefProxy):
            proxies.append(name)

    new_module = type(module_name, (ModuleType, ModuleProxy), {})(module_name)  # ModuleProxy
    new_module.bind(module_real, proxies)

    modules[module_name] = new_module