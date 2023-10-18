def _expand_str(path_cfg, alias_dict, overriding_kargs):
    """expand a path config given as a string

    """

    if path_cfg in alias_dict:
        # e.g., path_cfg = 'var_cut'
        return _expand_str_alias(path_cfg, alias_dict, overriding_kargs)

    # e.g., path_cfg = 'ev : {low} <= ev.var[0] < {high}'
    return _expand_for_lambda_str(path_cfg, alias_dict, overriding_kargs)