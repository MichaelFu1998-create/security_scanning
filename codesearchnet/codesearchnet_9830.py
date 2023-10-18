def get_vehicle_hours_by_type(gtfs, route_type):
    """
    Return the sum of vehicle hours in a particular day by route type.
    """

    day = gtfs.get_suitable_date_for_daily_extract()
    query = (" SELECT * , SUM(end_time_ds - start_time_ds)/3600 as vehicle_hours_type"
             " FROM"
             " (SELECT * FROM day_trips as q1"
             " INNER JOIN"
             " (SELECT route_I, type FROM routes) as q2"
             " ON q1.route_I = q2.route_I"
             " WHERE type = {route_type}"
             " AND date = '{day}')".format(day=day, route_type=route_type))
    df = gtfs.execute_custom_query_pandas(query)
    return df['vehicle_hours_type'].item()