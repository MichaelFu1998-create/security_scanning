def _expand_tuple(path_cfg, alias_dict, overriding_kargs):
    """expand a path config given as a tuple

    """

    # e.g.,
    # path_cfg = ('ev : {low} <= ev.var[0] < {high}', {'low': 10, 'high': 200})
    # overriding_kargs = {'alias': 'var_cut', 'name': 'var_cut25', 'low': 25}

    new_path_cfg = path_cfg[0]
    # e.g., 'ev : {low} <= ev.var[0] < {high}'

    new_overriding_kargs = path_cfg[1].copy()
    # e.g., {'low': 10, 'high': 200}

    new_overriding_kargs.update(overriding_kargs)
    # e.g., {'low': 25, 'high': 200, 'alias': 'var_cut', 'name': 'var_cut25'}

    return expand_path_cfg(
        new_path_cfg,
        overriding_kargs=new_overriding_kargs,
        alias_dict=alias_dict
    )