def get_tool_names():
    """ Get tool names from all configured groups.

    :return: list of tool names
    """
    names = []
    for group in cfg.get('Gromacs', 'groups').split():
        names.extend(cfg.get('Gromacs', group).split())
    return names