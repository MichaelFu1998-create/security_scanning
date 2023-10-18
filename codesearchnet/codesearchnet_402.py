def gen_round_trip_stats(round_trips):
    """Generate various round-trip statistics.

    Parameters
    ----------
    round_trips : pd.DataFrame
        DataFrame with one row per round trip trade.
        - See full explanation in round_trips.extract_round_trips

    Returns
    -------
    stats : dict
       A dictionary where each value is a pandas DataFrame containing
       various round-trip statistics.

    See also
    --------
    round_trips.print_round_trip_stats
    """

    stats = {}
    stats['pnl'] = agg_all_long_short(round_trips, 'pnl', PNL_STATS)
    stats['summary'] = agg_all_long_short(round_trips, 'pnl',
                                          SUMMARY_STATS)
    stats['duration'] = agg_all_long_short(round_trips, 'duration',
                                           DURATION_STATS)
    stats['returns'] = agg_all_long_short(round_trips, 'returns',
                                          RETURN_STATS)

    stats['symbols'] = \
        round_trips.groupby('symbol')['returns'].agg(RETURN_STATS).T

    return stats