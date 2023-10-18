def format_objects(objects, children=False, columns=None, header=True):
    '''Format a list of environments and modules for terminal output'''

    columns = columns or ('NAME', 'TYPE', 'PATH')
    objects = sorted(objects, key=_type_and_name)
    data = []
    for obj in objects:
        if isinstance(obj, cpenv.VirtualEnvironment):
            data.append(get_info(obj))
            modules = obj.get_modules()
            if children and modules:
                for mod in modules:
                    data.append(get_info(mod, indent=2, root=obj.path))
        else:
            data.append(get_info(obj))

    maxes = [len(max(col, key=len)) for col in zip(*data)]
    tmpl = '{:%d}  {:%d}  {:%d}' % tuple(maxes)
    lines = []
    if header:
        lines.append('\n' + bold_blue(tmpl.format(*columns)))

    for obj_data in data:
        lines.append(tmpl.format(*obj_data))

    return '\n'.join(lines)