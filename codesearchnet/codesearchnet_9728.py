def validate_day_start_ut(conn):
    """This validates the day_start_ut of the days table."""
    G = GTFS(conn)
    cur = conn.execute('SELECT date, day_start_ut FROM days')
    for date, day_start_ut in cur:
        #print date, day_start_ut
        assert day_start_ut == G.get_day_start_ut(date)