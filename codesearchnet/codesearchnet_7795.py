def _detect_migration_layout(vars, apps):
    """
    Detect migrations layout for plugins
    :param vars: installer settings
    :param apps: installed applications
    """
    DJANGO_MODULES = {}

    for module in vars.MIGRATIONS_CHECK_MODULES:
        if module in apps:
            try:
                mod = __import__('{0}.migrations_django'.format(module))  # NOQA
                DJANGO_MODULES[module] = '{0}.migrations_django'.format(module)
            except Exception:
                pass
    return DJANGO_MODULES