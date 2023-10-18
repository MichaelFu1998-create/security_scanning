def get_modules():
    '''Returns a list of available modules.'''

    modules = set()

    cwd = os.getcwd()
    for d in os.listdir(cwd):

        if d == 'module.yml':
            modules.add(Module(cwd))

        path = unipath(cwd, d)
        if utils.is_module(path):
            modules.add(Module(cwd))

    module_paths = get_module_paths()
    for module_path in module_paths:
        for d in os.listdir(module_path):

            path = unipath(module_path, d)
            if utils.is_module(path):
                modules.add(Module(path))

    return sorted(list(modules), key=lambda x: x.name)