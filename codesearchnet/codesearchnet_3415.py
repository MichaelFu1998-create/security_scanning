def save(f):
    """
    Save current config state to an yml file stream identified by |f|

    :param f: where to write the config file
    """
    global _groups

    c = {}
    for group_name, group in _groups.items():
        section = {var.name: var.value for var in group.updated_vars()}
        if not section:
            continue
        c[group_name] = section

    yaml.safe_dump(c, f, line_break=True)