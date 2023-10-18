def get_short_module_name(module_name, obj_name):
    """ Get the shortest possible module name """
    parts = module_name.split('.')
    short_name = module_name
    for i in range(len(parts) - 1, 0, -1):
        short_name = '.'.join(parts[:i])
        try:
            exec('from %s import %s' % (short_name, obj_name))
        except ImportError:
            # get the last working module name
            short_name = '.'.join(parts[:(i + 1)])
            break
    return short_name