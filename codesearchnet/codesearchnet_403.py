def print_round_trip_stats(round_trips, hide_pos=False):
    """Print various round-trip statistics. Tries to pretty-print tables
    with HTML output if run inside IPython NB.

    Parameters
    ----------
    round_trips : pd.DataFrame
        DataFrame with one row per round trip trade.
        - See full explanation in round_trips.extract_round_trips

    See also
    --------
    round_trips.gen_round_trip_stats
    """

    stats = gen_round_trip_stats(round_trips)

    print_table(stats['summary'], float_format='{:.2f}'.format,
                name='Summary stats')
    print_table(stats['pnl'], float_format='${:.2f}'.format, name='PnL stats')
    print_table(stats['duration'], float_format='{:.2f}'.format,
                name='Duration stats')
    print_table(stats['returns'] * 100, float_format='{:.2f}%'.format,
                name='Return stats')

    if not hide_pos:
        stats['symbols'].columns = stats['symbols'].columns.map(format_asset)
        print_table(stats['symbols'] * 100,
                    float_format='{:.2f}%'.format, name='Symbol stats')