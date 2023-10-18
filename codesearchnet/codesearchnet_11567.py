def _expand_str_alias(path_cfg, alias_dict, overriding_kargs):
    """expand a path config given as a string

    Args:
        path_cfg (str): an alias
        alias_dict (dict):
        overriding_kargs (dict):
    """

    # e.g.,
    # path_cfg = 'var_cut'

    new_path_cfg = alias_dict[path_cfg]
    # e.g., ('ev : {low} <= ev.var[0] < {high}', {'low': 10, 'high': 200})

    new_overriding_kargs = dict(alias=path_cfg)
    # e.g., {'alias': 'var_cut'}

    new_overriding_kargs.update(overriding_kargs)
    # e.g., {'alias': 'var_cut', 'name': 'var_cut25', 'low': 25}

    return expand_path_cfg(new_path_cfg, alias_dict,new_overriding_kargs)