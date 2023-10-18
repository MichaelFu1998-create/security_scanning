def temporal_network(gtfs,
                     start_time_ut=None,
                     end_time_ut=None,
                     route_type=None):
    """
    Compute the temporal network of the data, and return it as a pandas.DataFrame

    Parameters
    ----------
    gtfs : gtfspy.GTFS
    start_time_ut: int | None
        start time of the time span (in unix time)
    end_time_ut: int | None
        end time of the time span (in unix time)
    route_type: int | None
        Specifies which mode of public transport are included, or whether all modes should be included.
        The int should be one of the standard GTFS route_types:
        (see also gtfspy.route_types.TRANSIT_ROUTE_TYPES )
        If route_type is not specified, all modes are included.

    Returns
    -------
    events_df: pandas.DataFrame
        Columns: departure_stop, arrival_stop, departure_time_ut, arrival_time_ut, route_type, route_I, trip_I
    """
    events_df = gtfs.get_transit_events(start_time_ut=start_time_ut,
                                        end_time_ut=end_time_ut,
                                        route_type=route_type)
    events_df.drop('to_seq', 1, inplace=True)
    events_df.drop('shape_id', 1, inplace=True)
    events_df.drop('duration', 1, inplace=True)
    events_df.drop('route_id', 1, inplace=True)
    events_df.rename(
        columns={
            'from_seq': "seq"
        },
        inplace=True
    )
    return events_df