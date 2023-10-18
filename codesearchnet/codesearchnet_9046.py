def proc_elms(**kwargs) -> list:
    """
    Bloomberg overrides for elements

    Args:
        **kwargs: overrides

    Returns:
        list of tuples

    Examples:
        >>> proc_elms(PerAdj='A', Per='W')
        [('periodicityAdjustment', 'ACTUAL'), ('periodicitySelection', 'WEEKLY')]
        >>> proc_elms(Days='A', Fill='B')
        [('nonTradingDayFillOption', 'ALL_CALENDAR_DAYS'), ('nonTradingDayFillMethod', 'NIL_VALUE')]
        >>> proc_elms(CshAdjNormal=False, CshAdjAbnormal=True)
        [('adjustmentNormal', False), ('adjustmentAbnormal', True)]
        >>> proc_elms(Per='W', Quote='Average', start_date='2018-01-10')
        [('periodicitySelection', 'WEEKLY'), ('overrideOption', 'OVERRIDE_OPTION_GPA')]
        >>> proc_elms(QuoteType='Y')
        [('pricingOption', 'PRICING_OPTION_YIELD')]
        >>> proc_elms(QuoteType='Y', cache=True)
        [('pricingOption', 'PRICING_OPTION_YIELD')]
    """
    return [
        (ELEM_KEYS.get(k, k), ELEM_VALS.get(ELEM_KEYS.get(k, k), dict()).get(v, v))
        for k, v in kwargs.items()
        if (k in list(ELEM_KEYS.keys()) + list(ELEM_KEYS.values()))
        and (k not in PRSV_COLS)
    ]