def get_route_shape_segments(cur, route_id):
    """
    Given a route_id, return its stop-sequence.

    Parameters
    ----------
    cur: sqlite3.Cursor
        cursor to a GTFS database
    route_id: str
        id of the route

    Returns
    -------
    shape_points: list
        elements are dictionaries containing the 'seq', 'lat', and 'lon' of the shape
    """
    cur.execute('''SELECT seq, lat, lon
                    FROM (
                        SELECT shape_id
                        FROM route
                        LEFT JOIN trips
                        USING (route_I)
                        WHERE route_id=? limit 1
                        )
                    JOIN shapes
                    USING (shape_id)
                    ORDER BY seq''', (route_id,))
    shape_points = [dict(seq=row[0], lat=row[1], lon=row[2]) for row in cur]
    return shape_points