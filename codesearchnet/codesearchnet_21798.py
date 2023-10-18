def rem_active_module(module):
    '''Remove a module from CPENV_ACTIVE_MODULES environment variable'''

    modules = set(get_active_modules())
    modules.discard(module)
    new_modules_path = os.pathsep.join([m.path for m in modules])
    os.environ['CPENV_ACTIVE_MODULES'] = str(new_modules_path)