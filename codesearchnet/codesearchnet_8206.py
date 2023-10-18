def set_one(desc, name, value):
    """Set one section in a Project description"""
    old_value = desc.get(name)
    if old_value is None:
        raise KeyError('No section "%s"' % name)

    if value is None:
        value = type(old_value)()

    elif name in CLASS_SECTIONS:
        if isinstance(value, str):
            value = {'typename': aliases.resolve(value)}
        elif isinstance(value, type):
            value = {'typename': class_name.class_name(value)}
        elif not isinstance(value, dict):
            raise TypeError('Expected dict, str or type, got "%s"' % value)

        typename = value.get('typename')
        if typename:
            s = 's' if name == 'driver' else ''
            path = 'bibliopixel.' + name + s
            importer.import_symbol(typename, path)

    elif name == 'shape':
        if not isinstance(value, (list, int, tuple, str)):
            raise TypeError('Expected shape, got "%s"' % value)

    elif type(old_value) is not type(value):
        raise TypeError('Expected %s but got "%s" of type %s' %
                        (type(old_value), value, type(value)))

    desc[name] = value