def get_trip_points(cur, route_id, offset=0, tripid_glob=''):
    """Get all scheduled stops on a particular route_id.

    Given a route_id, return the trip-stop-list with
    latitude/longitudes.  This is a bit more tricky than it seems,
    because we have to go from table route->trips->stop_times.  This
    functions finds an arbitrary trip (in trip table) with this route ID
    and, and then returns all stop points for that trip.

    Parameters
    ----------
    cur : sqlite3.Cursor
        cursor to sqlite3 DB containing GTFS
    route_id : string or any
        route_id to get stop points of
    offset : int
        LIMIT offset if you don't want the first trip returned.
    tripid_glob : string
        If given, allows you to limit tripids which can be selected.
        Mainly useful in debugging.

    Returns
    -------
    stop-list
        List of stops in stop-seq format.
    """
    extra_where = ''
    if tripid_glob:
        extra_where = "AND trip_id GLOB '%s'" % tripid_glob
    cur.execute('SELECT seq, lat, lon '
                'FROM (select trip_I from route '
                '      LEFT JOIN trips USING (route_I) '
                '      WHERE route_id=? %s limit 1 offset ? ) '
                'JOIN stop_times USING (trip_I) '
                'LEFT JOIN stop USING (stop_id) '
                'ORDER BY seq' % extra_where, (route_id, offset))
    stop_points = [dict(seq=row[0], lat=row[1], lon=row[2]) for row in cur]
    return stop_points