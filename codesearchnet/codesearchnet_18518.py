def _data_integrity_check(data):
    """Checks if all command dependencies refers to and existing command. If not, a ProjectfileError
    will be raised with the problematic dependency and it's command.

    :param data: parsed raw data set.
    :return: None
    """
    deps = []
    for command in data['commands']:
        if 'dependencies' in data['commands'][command]:
            for d in data['commands'][command]['dependencies']:
                deps.append({
                    'd': d,
                    'c': command
                })
    for d in deps:
        if d['d'] not in data['commands']:
            raise error.ProjectfileError({
                'error': error.PROJECTFILE_INVALID_DEPENDENCY.format(d['d'], d['c'])
            })