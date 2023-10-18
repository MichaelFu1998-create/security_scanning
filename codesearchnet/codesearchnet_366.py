def compute_sector_exposures(positions, sectors, sector_dict=SECTORS):
    """
    Returns arrays of long, short and gross sector exposures of an algorithm's
    positions

    Parameters
    ----------
    positions : pd.DataFrame
        Daily equity positions of algorithm, in dollars.
        - See full explanation in compute_style_factor_exposures.

    sectors : pd.DataFrame
        Daily Morningstar sector code per asset
        - See full explanation in create_risk_tear_sheet

    sector_dict : dict or OrderedDict
        Dictionary of all sectors
        - Keys are sector codes (e.g. ints or strings) and values are sector
          names (which must be strings)
        - Defaults to Morningstar sectors
    """

    sector_ids = sector_dict.keys()

    long_exposures = []
    short_exposures = []
    gross_exposures = []
    net_exposures = []

    positions_wo_cash = positions.drop('cash', axis='columns')
    long_exposure = positions_wo_cash[positions_wo_cash > 0] \
        .sum(axis='columns')
    short_exposure = positions_wo_cash[positions_wo_cash < 0] \
        .abs().sum(axis='columns')
    gross_exposure = positions_wo_cash.abs().sum(axis='columns')

    for sector_id in sector_ids:
        in_sector = positions_wo_cash[sectors == sector_id]

        long_sector = in_sector[in_sector > 0] \
            .sum(axis='columns').divide(long_exposure)
        short_sector = in_sector[in_sector < 0] \
            .sum(axis='columns').divide(short_exposure)
        gross_sector = in_sector.abs().sum(axis='columns') \
            .divide(gross_exposure)
        net_sector = long_sector.subtract(short_sector)

        long_exposures.append(long_sector)
        short_exposures.append(short_sector)
        gross_exposures.append(gross_sector)
        net_exposures.append(net_sector)

    return long_exposures, short_exposures, gross_exposures, net_exposures