def expand_path_cfg(path_cfg, alias_dict={ }, overriding_kargs={ }):
    """expand a path config

    Args:
        path_cfg (str, tuple, dict): a config for path
        alias_dict (dict): a dict for aliases
        overriding_kargs (dict): to be used for recursive call
    """

    if isinstance(path_cfg, str):
        return _expand_str(path_cfg, alias_dict, overriding_kargs)

    if isinstance(path_cfg, dict):
        return _expand_dict(path_cfg, alias_dict)

    # assume tuple or list
    return _expand_tuple(path_cfg, alias_dict, overriding_kargs)