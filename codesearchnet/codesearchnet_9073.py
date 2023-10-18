def load_info(cat):
    """
    Load parameters for assets

    Args:
        cat: category

    Returns:
        dict

    Examples:
        >>> import pandas as pd
        >>>
        >>> assets = load_info(cat='assets')
        >>> all(cat in assets for cat in ['Equity', 'Index', 'Curncy', 'Corp'])
        True
        >>> os.environ['BBG_PATH'] = ''
        >>> exch = load_info(cat='exch')
        >>> pd.Series(exch['EquityUS']).allday
        [400, 2000]
        >>> test_root = f'{PKG_PATH}/tests'
        >>> os.environ['BBG_PATH'] = test_root
        >>> ovrd_exch = load_info(cat='exch')
        >>> # Somehow os.environ is not set properly in doctest environment
        >>> ovrd_exch.update(_load_yaml_(f'{test_root}/markets/exch.yml'))
        >>> pd.Series(ovrd_exch['EquityUS']).allday
        [300, 2100]
    """
    res = _load_yaml_(f'{PKG_PATH}/markets/{cat}.yml')
    root = os.environ.get('BBG_ROOT', '').replace('\\', '/')
    if not root: return res
    for cat, ovrd in _load_yaml_(f'{root}/markets/{cat}.yml').items():
        if isinstance(ovrd, dict):
            if cat in res: res[cat].update(ovrd)
            else: res[cat] = ovrd
        if isinstance(ovrd, list) and isinstance(res[cat], list): res[cat] += ovrd
    return res