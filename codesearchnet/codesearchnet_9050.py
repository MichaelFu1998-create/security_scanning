def info_qry(tickers, flds) -> str:
    """
    Logging info for given tickers and fields

    Args:
        tickers: tickers
        flds: fields

    Returns:
        str

    Examples:
        >>> print(info_qry(
        ...     tickers=['NVDA US Equity'], flds=['Name', 'Security_Name']
        ... ))
        tickers: ['NVDA US Equity']
        fields:  ['Name', 'Security_Name']
    """
    full_list = '\n'.join([f'tickers: {tickers[:8]}'] + [
        f'         {tickers[n:(n + 8)]}' for n in range(8, len(tickers), 8)
    ])
    return f'{full_list}\nfields:  {flds}'