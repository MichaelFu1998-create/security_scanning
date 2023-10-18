def modules_path_resolver(resolver, path):
    '''Resolves modules in CPENV_MODULES path and CPENV_HOME/modules'''

    from .api import get_module_paths

    for module_dir in get_module_paths():
        mod_path = unipath(module_dir, path)

        if is_module(mod_path):
            return Module(mod_path)

    raise ResolveError