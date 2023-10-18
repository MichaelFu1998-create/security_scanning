def get_sector_exposures(positions, symbol_sector_map):
    """
    Sum position exposures by sector.

    Parameters
    ----------
    positions : pd.DataFrame
        Contains position values or amounts.
        - Example
            index         'AAPL'         'MSFT'        'CHK'        cash
            2004-01-09    13939.380     -15012.993    -403.870      1477.483
            2004-01-12    14492.630     -18624.870    142.630       3989.610
            2004-01-13    -13853.280    13653.640     -100.980      100.000
    symbol_sector_map : dict or pd.Series
        Security identifier to sector mapping.
        Security ids as keys/index, sectors as values.
        - Example:
            {'AAPL' : 'Technology'
             'MSFT' : 'Technology'
             'CHK' : 'Natural Resources'}

    Returns
    -------
    sector_exp : pd.DataFrame
        Sectors and their allocations.
        - Example:
            index         'Technology'    'Natural Resources' cash
            2004-01-09    -1073.613       -403.870            1477.4830
            2004-01-12    -4132.240       142.630             3989.6100
            2004-01-13    -199.640        -100.980            100.0000
    """

    cash = positions['cash']
    positions = positions.drop('cash', axis=1)

    unmapped_pos = np.setdiff1d(positions.columns.values,
                                list(symbol_sector_map.keys()))
    if len(unmapped_pos) > 0:
        warn_message = """Warning: Symbols {} have no sector mapping.
        They will not be included in sector allocations""".format(
            ", ".join(map(str, unmapped_pos)))
        warnings.warn(warn_message, UserWarning)

    sector_exp = positions.groupby(
        by=symbol_sector_map, axis=1).sum()

    sector_exp['cash'] = cash

    return sector_exp