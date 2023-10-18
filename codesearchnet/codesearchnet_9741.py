def get_shape_points(cur, shape_id):
    """
    Given a shape_id, return its shape-sequence.

    Parameters
    ----------
    cur: sqlite3.Cursor
        cursor to a GTFS database
    shape_id: str
        id of the route

    Returns
    -------
    shape_points: list
        elements are dictionaries containing the 'seq', 'lat', and 'lon' of the shape
    """
    cur.execute('''SELECT seq, lat, lon, d FROM shapes where shape_id=?
                    ORDER BY seq''', (shape_id,))
    shape_points = [dict(seq=row[0], lat=row[1], lon=row[2], d=row[3])
                    for row in cur]
    return shape_points