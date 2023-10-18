def route_frequencies(gtfs, results_by_mode=False):
    """
    Return the frequency of all types of routes per day.

    Parameters
    -----------
    gtfs: GTFS

    Returns
    -------
    pandas.DataFrame with columns
        route_I, type, frequency
    """
    day = gtfs.get_suitable_date_for_daily_extract()
    query = (
        " SELECT f.route_I, type, frequency FROM routes as r"
        " JOIN"
        " (SELECT route_I, COUNT(route_I) as frequency"
        " FROM"
        " (SELECT date, route_I, trip_I"
        " FROM day_stop_times"
        " WHERE date = '{day}'"
        " GROUP by route_I, trip_I)"
        " GROUP BY route_I) as f"
        " ON f.route_I = r.route_I"
        " ORDER BY frequency DESC".format(day=day))
    
    return pd.DataFrame(gtfs.execute_custom_query_pandas(query))