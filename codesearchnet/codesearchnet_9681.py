def remove_all_trips_fully_outside_buffer(db_conn, center_lat, center_lon, buffer_km, update_secondary_data=True):
    """
    Not used in the regular filter process for the time being.

    Parameters
    ----------
    db_conn: sqlite3.Connection
        connection to the GTFS object
    center_lat: float
    center_lon: float
    buffer_km: float
    """
    distance_function_str = add_wgs84_distance_function_to_db(db_conn)
    stops_within_buffer_query_sql = "SELECT stop_I FROM stops WHERE CAST(" + distance_function_str + \
                                "(lat, lon, {lat} , {lon}) AS INT) < {d_m}"\
        .format(lat=float(center_lat), lon=float(center_lon), d_m=int(1000*buffer_km))
    select_all_trip_Is_where_stop_I_is_within_buffer_sql = "SELECT distinct(trip_I) FROM stop_times WHERE stop_I IN (" + stops_within_buffer_query_sql + ")"
    trip_Is_to_remove_sql = "SELECT trip_I FROM trips WHERE trip_I NOT IN ( " + select_all_trip_Is_where_stop_I_is_within_buffer_sql + ")"
    trip_Is_to_remove = pandas.read_sql(trip_Is_to_remove_sql, db_conn)["trip_I"].values
    trip_Is_to_remove_string = ",".join([str(trip_I) for trip_I in trip_Is_to_remove])
    remove_all_trips_fully_outside_buffer_sql = "DELETE FROM trips WHERE trip_I IN (" + trip_Is_to_remove_string + ")"
    remove_all_stop_times_where_trip_I_fully_outside_buffer_sql = "DELETE FROM stop_times WHERE trip_I IN (" + trip_Is_to_remove_string  + ")"
    db_conn.execute(remove_all_trips_fully_outside_buffer_sql)
    db_conn.execute(remove_all_stop_times_where_trip_I_fully_outside_buffer_sql)
    delete_stops_not_in_stop_times_and_not_as_parent_stop(db_conn)
    db_conn.execute(DELETE_ROUTES_NOT_PRESENT_IN_TRIPS_SQL)
    db_conn.execute(DELETE_SHAPES_NOT_REFERENCED_IN_TRIPS_SQL)
    db_conn.execute(DELETE_DAYS_ENTRIES_NOT_PRESENT_IN_TRIPS_SQL)
    db_conn.execute(DELETE_DAY_TRIPS2_ENTRIES_NOT_PRESENT_IN_TRIPS_SQL)
    db_conn.execute(DELETE_CALENDAR_ENTRIES_FOR_NON_REFERENCE_SERVICE_IS_SQL)
    db_conn.execute(DELETE_CALENDAR_DATES_ENTRIES_FOR_NON_REFERENCE_SERVICE_IS_SQL)
    db_conn.execute(DELETE_FREQUENCIES_ENTRIES_NOT_PRESENT_IN_TRIPS)
    db_conn.execute(DELETE_AGENCIES_NOT_REFERENCED_IN_ROUTES_SQL)
    if update_secondary_data:
        update_secondary_data_copies(db_conn)