def _feed_calendar_span(gtfs, stats):
    """
    Computes the temporal coverage of each source feed

    Parameters
    ----------
    gtfs: gtfspy.GTFS object
    stats: dict
        where to append the stats

    Returns
    -------
    stats: dict
    """
    n_feeds = _n_gtfs_sources(gtfs)[0]
    max_start = None
    min_end = None
    if n_feeds > 1:
        for i in range(n_feeds):
            feed_key = "feed_" + str(i) + "_"
            start_key = feed_key + "calendar_start"
            end_key = feed_key + "calendar_end"
            calendar_span = gtfs.conn.cursor().execute(
                'SELECT min(date), max(date) FROM trips, days '
                'WHERE trips.trip_I = days.trip_I AND trip_id LIKE ?;', (feed_key + '%',)).fetchone()

            stats[start_key] = calendar_span[0]
            stats[end_key] = calendar_span[1]
            if calendar_span[0] is not None and calendar_span[1] is not None:
                if not max_start and not min_end:
                    max_start = calendar_span[0]
                    min_end = calendar_span[1]
                else:
                    if gtfs.get_day_start_ut(calendar_span[0]) > gtfs.get_day_start_ut(max_start):
                        max_start = calendar_span[0]
                    if gtfs.get_day_start_ut(calendar_span[1]) < gtfs.get_day_start_ut(min_end):
                        min_end = calendar_span[1]
        stats["latest_feed_start_date"] = max_start
        stats["earliest_feed_end_date"] = min_end
    else:
        stats["latest_feed_start_date"] = stats["start_date"]
        stats["earliest_feed_end_date"] = stats["end_date"]
    return stats