def _fleet_size_estimate(gtfs, hour, date):
    """
    Calculates fleet size estimates by two separate formula:
     1. Considering all routes separately with no interlining and doing a deficit calculation at every terminal
     2. By looking at the maximum number of vehicles in simultaneous movement

    Parameters
    ----------
    gtfs: GTFS
    hour: int
    date: ?

    Returns
    -------
    results: dict
        a dict with keys:
            fleet_size_route_based
            fleet_size_max_movement

    """
    results = {}

    fleet_size_list = []
    cur = gtfs.conn.cursor()
    rows = cur.execute(
        'SELECT type, max(vehicles) '
        'FROM ('
        'SELECT type, direction_id, sum(vehicles) as vehicles '
        'FROM '
        '('
        'SELECT trips.route_I, trips.direction_id, routes.route_id, name, type, count(*) as vehicles, cycle_time_min '
        'FROM trips, routes, days, '
        '('
        'SELECT first_trip.route_I, first_trip.direction_id, first_trip_start_time, first_trip_end_time, '
        'MIN(start_time_ds) as return_trip_start_time, end_time_ds as return_trip_end_time, '
        '(end_time_ds - first_trip_start_time)/60 as cycle_time_min '
        'FROM '
        'trips, '
        '(SELECT route_I, direction_id, MIN(start_time_ds) as first_trip_start_time, '
        'end_time_ds as first_trip_end_time '
        'FROM trips, days '
        'WHERE trips.trip_I=days.trip_I AND start_time_ds >= ? * 3600 '
        'AND start_time_ds <= (? + 1) * 3600 AND date = ? '
        'GROUP BY route_I, direction_id) first_trip '
        'WHERE first_trip.route_I = trips.route_I '
        'AND first_trip.direction_id != trips.direction_id '
        'AND start_time_ds >= first_trip_end_time '
        'GROUP BY trips.route_I, trips.direction_id'
        ') return_trip '
        'WHERE trips.trip_I=days.trip_I AND trips.route_I= routes.route_I '
        'AND date = ? AND trips.route_I = return_trip.route_I '
        'AND trips.direction_id = return_trip.direction_id '
        'AND start_time_ds >= first_trip_start_time '
        'AND start_time_ds < return_trip_end_time '
        'GROUP BY trips.route_I, trips.direction_id '
        'ORDER BY type, name, vehicles desc'
        ') cycle_times '
        'GROUP BY direction_id, type'
        ') vehicles_type '
        'GROUP BY type;', (hour, hour, date, date))
    for row in rows:
        fleet_size_list.append(str(row[0]) + ':' + str(row[1]))
    results['fleet_size_route_based'] = " ".join(fleet_size_list)

    # Fleet size estimate: maximum number of vehicles in movement
    fleet_size_list = []
    fleet_size_dict = {}
    if hour:
        for minute in range(hour * 3600, (hour + 1) * 3600, 60):
            rows = gtfs.conn.cursor().execute(
                'SELECT type, count(*) '
                'FROM trips, routes, days '
                'WHERE trips.route_I = routes.route_I '
                'AND trips.trip_I=days.trip_I '
                'AND start_time_ds <= ? '
                'AND end_time_ds > ? + 60 '
                'AND date = ? '
                'GROUP BY type;',
                (minute, minute, date))

            for row in rows:
                if fleet_size_dict.get(row[0], 0) < row[1]:
                    fleet_size_dict[row[0]] = row[1]

    for key in fleet_size_dict.keys():
        fleet_size_list.append(str(key) + ':' + str(fleet_size_dict[key]))
    results["fleet_size_max_movement"] = ' '.join(fleet_size_list)
    return results