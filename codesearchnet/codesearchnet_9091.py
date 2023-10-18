def missing_info(**kwargs) -> str:
    """
    Full infomation for missing query
    """
    func = kwargs.pop('func', 'unknown')
    if 'ticker' in kwargs: kwargs['ticker'] = kwargs['ticker'].replace('/', '_')
    info = utils.to_str(kwargs, fmt='{value}', sep='/')[1:-1]
    return f'{func}/{info}'