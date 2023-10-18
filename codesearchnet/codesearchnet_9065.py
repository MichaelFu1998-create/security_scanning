def market_info(ticker: str) -> dict:
    """
    Get info for given market

    Args:
        ticker: Bloomberg full ticker

    Returns:
        dict

    Examples:
        >>> info = market_info('SHCOMP Index')
        >>> info['exch']
        'EquityChina'
        >>> info = market_info('ICICIC=1 IS Equity')
        >>> info['freq'], info['is_fut']
        ('M', True)
        >>> info = market_info('INT1 Curncy')
        >>> info['freq'], info['is_fut']
        ('M', True)
        >>> info = market_info('CL1 Comdty')
        >>> info['freq'], info['is_fut']
        ('M', True)
        >>> # Wrong tickers
        >>> market_info('C XX Equity')
        {}
        >>> market_info('XXX Comdty')
        {}
        >>> market_info('Bond_ISIN Corp')
        {}
        >>> market_info('XYZ Index')
        {}
        >>> market_info('XYZ Curncy')
        {}
    """
    t_info = ticker.split()
    assets = param.load_info('assets')

    # ========================== #
    #           Equity           #
    # ========================== #

    if (t_info[-1] == 'Equity') and ('=' not in t_info[0]):
        exch = t_info[-2]
        for info in assets.get('Equity', [dict()]):
            if 'exch_codes' not in info: continue
            if exch in info['exch_codes']: return info
        return dict()

    # ============================ #
    #           Currency           #
    # ============================ #

    if t_info[-1] == 'Curncy':
        for info in assets.get('Curncy', [dict()]):
            if 'tickers' not in info: continue
            if (t_info[0].split('+')[0] in info['tickers']) or \
                    (t_info[0][-1].isdigit() and (t_info[0][:-1] in info['tickers'])):
                return info
        return dict()

    if t_info[-1] == 'Comdty':
        for info in assets.get('Comdty', [dict()]):
            if 'tickers' not in info: continue
            if t_info[0][:-1] in info['tickers']: return info
        return dict()

    # =================================== #
    #           Index / Futures           #
    # =================================== #

    if (t_info[-1] == 'Index') or (
        (t_info[-1] == 'Equity') and ('=' in t_info[0])
    ):
        if t_info[-1] == 'Equity':
            tck = t_info[0].split('=')[0]
        else:
            tck = ' '.join(t_info[:-1])
        for info in assets.get('Index', [dict()]):
            if 'tickers' not in info: continue
            if (tck[:2] == 'UX') and ('UX' in info['tickers']): return info
            if tck in info['tickers']:
                if t_info[-1] == 'Equity': return info
                if not info.get('is_fut', False): return info
            if tck[:-1].rstrip() in info['tickers']:
                if info.get('is_fut', False): return info
        return dict()

    if t_info[-1] == 'Corp':
        for info in assets.get('Corp', [dict()]):
            if 'ticker' not in info: continue

    return dict()