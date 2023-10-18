def find_best_segments(cur, stops, shape_ids, route_id=None,
                       breakpoints_cache=None):
    """Finds the best shape_id for a stop-sequence.

    This is used in cases like when you have GPS data with a route
    name, but you don't know the route direction.  It tries shapes
    going both directions and returns the shape that best matches.
    Could be used in other cases as well.

    Parameters
    ----------
    cur : sqlite3.Cursor
        database cursor
    stops : list
    shape_ids : list of shape_id:s
    route_id : route_id to search for stops
    breakpoints_cache : dict
        If given, use this to cache results from this function.
    """
    cache_key = None
    if breakpoints_cache is not None:
        # Calculate a cache key for this sequence.  If shape_id and
        # all stop_Is are the same, then we assume that it is the same
        # route and re-use existing breakpoints.
        cache_key = (route_id, tuple(x['stop_I'] for x in stops))
        if cache_key in breakpoints_cache:
            print('found in cache')
            return breakpoints_cache[cache_key]

    if route_id is not None:
        cur.execute('''SELECT DISTINCT shape_id
                        FROM routes
                        LEFT JOIN trips
                        USING (route_I)
                        WHERE route_id=?''',
                    (route_id,))
        data = cur.fetchall()
        # If not data, then route_id didn't match anything, or there
        # were no shapes defined.  We have to exit in this case.
        if not data:
            print("No data for route_id=%s" % route_id)
            return [], None, None, None
        #
        shape_ids = zip(*data)[0]
    # print 'find_best_segments:', shape_ids
    results = []
    for shape_id in shape_ids:
        shape = get_shape_points(cur, shape_id)
        breakpoints, badness = find_segments(stops, shape)
        results.append([badness, breakpoints, shape, shape_id])
        if len(stops) > 5 and badness < 5*(len(stops)):
            break

    best = np.argmin(zip(*results)[0])
    # print 'best', best
    badness = results[best][0]
    breakpoints = results[best][1]
    shape = results[best][2]
    shape_id = results[best][3]
    if breakpoints_cache is not None:
        print("storing in cache", cache_key[0], hash(cache_key[1:]))
        breakpoints_cache[cache_key] = breakpoints, badness, shape, shape_id
    return breakpoints, badness, shape, shape_id