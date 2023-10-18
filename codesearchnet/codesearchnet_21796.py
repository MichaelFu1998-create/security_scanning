def get_active_modules():
    ''':returns: a list of active :class:`Module` s or []'''

    modules = os.environ.get('CPENV_ACTIVE_MODULES', None)
    if modules:
        modules = modules.split(os.pathsep)
        return [Module(module) for module in modules]

    return []