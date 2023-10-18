def get_shape_between_stops(cur, trip_I, seq_stop1=None, seq_stop2=None, shape_breaks=None):
    """
    Given a trip_I (shortened id), return shape points between two stops
    (seq_stop1 and seq_stop2).

    Trip_I is used for matching obtaining the full shape of one trip (route).
    From the resulting shape we then obtain only shape points between
    stop_seq1 and stop_seq2
    trip_I---(trips)--->shape_id
    trip_I, seq_stop1----(stop_times)---> shape_break1
    trip_I, seq_stop2----(stop_times)---> shape_break2
    shapes_id+shape_break1+shape_break2 --(shapes)--> result

    Parameters
    ----------
    cur : sqlite3.Cursor
        cursor to sqlite3 DB containing GTFS
    trip_I : int
        transformed trip_id (i.e. a new column that is created when
        GTFS is imported to a DB)
    seq_stop1: int
        a positive inger describing the index of the point of the shape that
        corresponds to the first stop
    seq_stop2: int
        a positive inger describing the index of the point of the shape that
        corresponds to the second stop
    shape_breaks: ??

    Returns
    -------
    shapedict: dict
        Dictionary containing the latitudes and longitudes:
            lats=shapedict['lat']
            lons=shapedict['lon']
    """

    assert (seq_stop1 and seq_stop2) or shape_breaks
    if not shape_breaks:
        shape_breaks = []
        for seq_stop in [seq_stop1, seq_stop2]:
            query = """SELECT shape_break FROM stop_times
                        WHERE trip_I=%d AND seq=%d
                    """ % (trip_I, seq_stop)
            for row in cur.execute(query):
                shape_breaks.append(row[0])
    assert len(shape_breaks) == 2

    query = """SELECT seq, lat, lon
                FROM (SELECT shape_id FROM trips WHERE trip_I=%d)
                JOIN shapes USING (shape_id)
                WHERE seq>=%d AND seq <= %d;
            """ % (trip_I, shape_breaks[0], shape_breaks[1])
    shapedict = {'lat': [], 'lon': [], 'seq': []}
    for row in cur.execute(query):
        shapedict['seq'].append(row[0])
        shapedict['lat'].append(row[1])
        shapedict['lon'].append(row[2])
    return shapedict