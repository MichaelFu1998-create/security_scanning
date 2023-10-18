def ccy_pair(local, base='USD') -> CurrencyPair:
    """
    Currency pair info

    Args:
        local: local currency
        base: base currency

    Returns:
        CurrencyPair

    Examples:
        >>> ccy_pair(local='HKD', base='USD')
        CurrencyPair(ticker='HKD Curncy', factor=1.0, power=1)
        >>> ccy_pair(local='GBp')
        CurrencyPair(ticker='GBP Curncy', factor=100, power=-1)
        >>> ccy_pair(local='USD', base='GBp')
        CurrencyPair(ticker='GBP Curncy', factor=0.01, power=1)
        >>> ccy_pair(local='XYZ', base='USD')
        CurrencyPair(ticker='', factor=1.0, power=1)
        >>> ccy_pair(local='GBP', base='GBp')
        CurrencyPair(ticker='', factor=0.01, power=1)
        >>> ccy_pair(local='GBp', base='GBP')
        CurrencyPair(ticker='', factor=100.0, power=1)
    """
    ccy_param = param.load_info(cat='ccy')
    if f'{local}{base}' in ccy_param:
        info = ccy_param[f'{local}{base}']

    elif f'{base}{local}' in ccy_param:
        info = ccy_param[f'{base}{local}']
        info['factor'] = 1. / info.get('factor', 1.)
        info['power'] = -info.get('power', 1)

    elif base.lower() == local.lower():
        info = dict(ticker='')
        info['factor'] = 1.
        if base[-1].lower() == base[-1]:
            info['factor'] /= 100.
        if local[-1].lower() == local[-1]:
            info['factor'] *= 100.

    else:
        logger = logs.get_logger(ccy_pair)
        logger.error(f'incorrect currency - local {local} / base {base}')
        return CurrencyPair(ticker='', factor=1., power=1)

    if 'factor' not in info: info['factor'] = 1.
    if 'power' not in info: info['power'] = 1
    return CurrencyPair(**info)