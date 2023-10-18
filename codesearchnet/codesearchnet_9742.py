def get_shape_points2(cur, shape_id):
    """
    Given a shape_id, return its shape-sequence (as a dict of lists).
    get_shape_points function returns them as a list of dicts

    Parameters
    ----------
    cur: sqlite3.Cursor
        cursor to a GTFS database
    shape_id: str
        id of the route

    Returns
    -------
    shape_points: dict of lists
        dict contains keys 'seq', 'lat', 'lon', and 'd'(istance) of the shape
    """
    cur.execute('''SELECT seq, lat, lon, d FROM shapes where shape_id=?
                    ORDER BY seq''', (shape_id,))
    shape_points = {'seqs': [], 'lats':  [], 'lons': [], 'd': []}
    for row in cur:
        shape_points['seqs'].append(row[0])
        shape_points['lats'].append(row[1])
        shape_points['lons'].append(row[2])
        shape_points['d'].append(row[3])
    return shape_points