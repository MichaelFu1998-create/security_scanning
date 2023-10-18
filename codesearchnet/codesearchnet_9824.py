def get_stats(gtfs):
    """
    Get basic statistics of the GTFS data.

    Parameters
    ----------
    gtfs: GTFS

    Returns
    -------
    stats: dict
        A dictionary of various statistics.
        Keys should be strings, values should be inputtable to a database (int, date, str, ...)
        (but not a list)
    """
    stats = {}
    # Basic table counts
    for table in ['agencies', 'routes', 'stops', 'stop_times', 'trips', 'calendar', 'shapes', 'calendar_dates',
                  'days', 'stop_distances', 'frequencies', 'feed_info', 'transfers']:
        stats["n_" + table] = gtfs.get_row_count(table)

    # Agency names
    agencies = gtfs.get_table("agencies")
    stats["agencies"] = "_".join(agencies['name'].values)

    # Stop lat/lon range
    stops = gtfs.get_table("stops")
    lats = stops['lat'].values
    lons = stops['lon'].values
    percentiles = [0, 10, 50, 90, 100]

    try:
        lat_percentiles = numpy.percentile(lats, percentiles)
    except IndexError:
        lat_percentiles = [None] * 5
    lat_min, lat_10, lat_median, lat_90, lat_max = lat_percentiles
    stats["lat_min"] = lat_min
    stats["lat_10"] = lat_10
    stats["lat_median"] = lat_median
    stats["lat_90"] = lat_90
    stats["lat_max"] = lat_max

    try:
        lon_percentiles = numpy.percentile(lons, percentiles)
    except IndexError:
        lon_percentiles = [None] * 5
    lon_min, lon_10, lon_median, lon_90, lon_max = lon_percentiles
    stats["lon_min"] = lon_min
    stats["lon_10"] = lon_10
    stats["lon_median"] = lon_median
    stats["lon_90"] = lon_90
    stats["lon_max"] = lon_max

    if len(lats) > 0:
        stats["height_km"] = wgs84_distance(lat_min, lon_median, lat_max, lon_median) / 1000.
        stats["width_km"] = wgs84_distance(lon_min, lat_median, lon_max, lat_median) / 1000.
    else:
        stats["height_km"] = None
        stats["width_km"] = None

    first_day_start_ut, last_day_start_ut = gtfs.get_day_start_ut_span()
    stats["start_time_ut"] = first_day_start_ut
    if last_day_start_ut is None:
        stats["end_time_ut"] = None
    else:
        # 28 (instead of 24) comes from the GTFS stANDard
        stats["end_time_ut"] = last_day_start_ut + 28 * 3600

    stats["start_date"] = gtfs.get_min_date()
    stats["end_date"] = gtfs.get_max_date()

    # Maximum activity day
    max_activity_date = gtfs.execute_custom_query(
        'SELECT count(*), date '
        'FROM days '
        'GROUP BY date '
        'ORDER BY count(*) DESC, date '
        'LIMIT 1;').fetchone()
    if max_activity_date:
        stats["max_activity_date"] = max_activity_date[1]
        max_activity_hour = gtfs.get_cursor().execute(
            'SELECT count(*), arr_time_hour FROM day_stop_times '
            'WHERE date=? GROUP BY arr_time_hour '
            'ORDER BY count(*) DESC;', (stats["max_activity_date"],)).fetchone()
        if max_activity_hour:
            stats["max_activity_hour"] = max_activity_hour[1]
        else:
            stats["max_activity_hour"] = None

    # Fleet size estimate: considering each line separately
    if max_activity_date and max_activity_hour:
        fleet_size_estimates = _fleet_size_estimate(gtfs, stats['max_activity_hour'], stats['max_activity_date'])
        stats.update(fleet_size_estimates)

    # Compute simple distributions of various columns that have a finite range of values.
    # Commented lines refer to values that are not imported yet, ?

    stats['routes__type__dist'] = _distribution(gtfs, 'routes', 'type')
    # stats['stop_times__pickup_type__dist'] = _distribution(gtfs, 'stop_times', 'pickup_type')
    # stats['stop_times__drop_off_type__dist'] = _distribution(gtfs, 'stop_times', 'drop_off_type')
    # stats['stop_times__timepoint__dist'] = _distribution(gtfs, 'stop_times', 'timepoint')
    stats['calendar_dates__exception_type__dist'] = _distribution(gtfs, 'calendar_dates', 'exception_type')
    stats['frequencies__exact_times__dist'] = _distribution(gtfs, 'frequencies', 'exact_times')
    stats['transfers__transfer_type__dist'] = _distribution(gtfs, 'transfers', 'transfer_type')
    stats['agencies__lang__dist'] = _distribution(gtfs, 'agencies', 'lang')
    stats['stops__location_type__dist'] = _distribution(gtfs, 'stops', 'location_type')
    # stats['stops__wheelchair_boarding__dist'] = _distribution(gtfs, 'stops', 'wheelchair_boarding')
    # stats['trips__wheelchair_accessible__dist'] = _distribution(gtfs, 'trips', 'wheelchair_accessible')
    # stats['trips__bikes_allowed__dist'] = _distribution(gtfs, 'trips', 'bikes_allowed')
    # stats[''] = _distribution(gtfs, '', '')
    stats = _feed_calendar_span(gtfs, stats)

    return stats