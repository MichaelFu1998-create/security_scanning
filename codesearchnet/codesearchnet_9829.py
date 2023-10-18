def hourly_frequencies(gtfs, st, et, route_type):
    """
    Return all the number of vehicles (i.e. busses,trams,etc) that pass hourly through a stop in a time frame.

    Parameters
    ----------
    gtfs: GTFS
    st : int
        start time of the time framein unix time
    et : int
        end time of the time frame in unix time
    route_type: int

    Returns
    -------
    numeric pandas.DataFrame with columns
        stop_I, lat, lon, frequency
    """ 
    timeframe = et-st
    hours = timeframe/ 3600
    day = gtfs.get_suitable_date_for_daily_extract()
    stops = gtfs.get_stops_for_route_type(route_type).T.drop_duplicates().T
    query = ("SELECT * FROM stops as x"
             " JOIN"
             " (SELECT * , COUNT(*)/{h} as frequency"
             " FROM stop_times, days"
             " WHERE stop_times.trip_I = days.trip_I"
             " AND dep_time_ds > {st}"
             " AND dep_time_ds < {et}"
             " AND date = '{day}'"
             " GROUP BY stop_I) as y"
             " ON y.stop_I = x.stop_I".format(h=hours, st=st, et=et, day=day))
    try:
        trips_frequency = gtfs.execute_custom_query_pandas(query).T.drop_duplicates().T
        df = pd.merge(stops[['stop_I', 'lat', 'lon']], trips_frequency[['stop_I', 'frequency']],
                      on='stop_I', how='inner')
        return df.apply(pd.to_numeric)
    except:
        raise ValueError("Maybe too short time frame!")