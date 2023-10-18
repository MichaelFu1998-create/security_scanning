def get_module_paths():
    ''':returns: paths in CPENV_MODULES env var and CPENV_HOME/modules'''

    module_paths = []

    cpenv_modules_path = os.environ.get('CPENV_MODULES', None)
    if cpenv_modules_path:
        module_paths.extend(cpenv_modules_path.split(os.pathsep))

    module_paths.append(unipath(get_home_path(), 'modules'))

    return module_paths