def remove_dangling_shapes(db_conn):
    """
    Remove dangling entries from the shapes directory.

    Parameters
    ----------
    db_conn: sqlite3.Connection
        connection to the GTFS object
    """
    db_conn.execute(DELETE_SHAPES_NOT_REFERENCED_IN_TRIPS_SQL)
    SELECT_MIN_MAX_SHAPE_BREAKS_BY_TRIP_I_SQL = \
        "SELECT trips.trip_I, shape_id, min(shape_break) as min_shape_break, max(shape_break) as max_shape_break FROM trips, stop_times WHERE trips.trip_I=stop_times.trip_I GROUP BY trips.trip_I"
    trip_min_max_shape_seqs= pandas.read_sql(SELECT_MIN_MAX_SHAPE_BREAKS_BY_TRIP_I_SQL, db_conn)

    rows = []
    for row in trip_min_max_shape_seqs.itertuples():
        shape_id, min_shape_break, max_shape_break = row.shape_id, row.min_shape_break, row.max_shape_break
        if min_shape_break is None or max_shape_break is None:
            min_shape_break = float('-inf')
            max_shape_break = float('-inf')
        rows.append( (shape_id, min_shape_break, max_shape_break) )
    DELETE_SQL_BASE = "DELETE FROM shapes WHERE shape_id=? AND (seq<? OR seq>?)"
    db_conn.executemany(DELETE_SQL_BASE, rows)
    remove_dangling_shapes_references(db_conn)