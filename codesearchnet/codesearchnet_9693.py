def calculate_trip_shape_breakpoints(conn):
    """Pre-compute the shape points corresponding to each trip's stop.

    Depends: shapes"""
    from gtfspy import shapes

    cur = conn.cursor()
    breakpoints_cache = {}

    # Counters for problems - don't print every problem.
    count_bad_shape_ordering = 0
    count_bad_shape_fit = 0
    count_no_shape_fit = 0

    trip_Is = [x[0] for x in
               cur.execute('SELECT DISTINCT trip_I FROM stop_times').fetchall()]
    for trip_I in trip_Is:
        # Get the shape points
        row = cur.execute('''SELECT shape_id
                                  FROM trips WHERE trip_I=?''', (trip_I,)).fetchone()
        if row is None:
            continue
        shape_id = row[0]
        if shape_id is None or shape_id == '':
            continue

        # Get the stop points
        cur.execute('''SELECT seq, lat, lon, stop_id
                       FROM stop_times LEFT JOIN stops USING (stop_I)
                       WHERE trip_I=?
                       ORDER BY seq''',
                    (trip_I,))
        #print '%20s, %s'%(run_code, datetime.fromtimestamp(run_sch_starttime))
        stop_points = [dict(seq=row[0],
                            lat=row[1],
                            lon=row[2],
                            stop_I=row[3])
                       for row in cur if row[1] and row[2]]
        # Calculate a cache key for this sequence.
        # If both shape_id, and all stop_Is are same, then we can re-use existing breakpoints:
        cache_key = (shape_id, tuple(x['stop_I'] for x in stop_points))
        if cache_key in breakpoints_cache:
            breakpoints = breakpoints_cache[cache_key]
        else:
            # Must re-calculate breakpoints:

            shape_points = shapes.get_shape_points(cur, shape_id)
            breakpoints, badness \
                = shapes.find_segments(stop_points, shape_points)
            if breakpoints != sorted(breakpoints):
                # route_name, route_id, route_I, trip_id, trip_I = \
                #    cur.execute('''SELECT name, route_id, route_I, trip_id, trip_I
                #                 FROM trips LEFT JOIN routes USING (route_I)
                #                 WHERE trip_I=? LIMIT 1''', (trip_I,)).fetchone()
                # print "Ignoring: Route with bad shape ordering:", route_name, route_id, route_I, trip_id, trip_I
                count_bad_shape_ordering += 1
                # select * from stop_times where trip_I=NNNN order by shape_break;
                breakpoints_cache[cache_key] = None
                continue  # Do not set shape_break for this trip.
            # Add it to cache
            breakpoints_cache[cache_key] = breakpoints

            if badness > 30 * len(breakpoints):
                #print "bad shape fit: %s (%s, %s, %s)" % (badness, trip_I, shape_id, len(breakpoints))
                count_bad_shape_fit += 1

        if breakpoints is None:
            continue

        if len(breakpoints) == 0:
            #  No valid route could be identified.
            #print "Ignoring: No shape identified for trip_I=%s, shape_id=%s" % (trip_I, shape_id)
            count_no_shape_fit += 1
            continue

        # breakpoints is the corresponding points for each stop
        assert len(breakpoints) == len(stop_points)
        cur.executemany('UPDATE stop_times SET shape_break=? '
                        'WHERE trip_I=? AND seq=? ',
                        ((int(bkpt), int(trip_I), int(stpt['seq']))
                         for bkpt, stpt in zip(breakpoints, stop_points)))
    if count_bad_shape_fit > 0:
        print(" Shape trip breakpoints: %s bad fits" % count_bad_shape_fit)
    if count_bad_shape_ordering > 0:
        print(" Shape trip breakpoints: %s bad shape orderings" % count_bad_shape_ordering)
    if count_no_shape_fit > 0:
        print(" Shape trip breakpoints: %s no shape fits" % count_no_shape_fit)
    conn.commit()