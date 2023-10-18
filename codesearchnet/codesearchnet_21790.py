def launch(module_name, *args, **kwargs):
    '''Activates and launches a module

    :param module_name: name of module to launch
    '''

    r = resolve(module_name)
    r.activate()
    mod = r.resolved[0]
    mod.launch(*args, **kwargs)