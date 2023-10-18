def stop_to_stop_network_for_route_type(gtfs,
                                        route_type,
                                        link_attributes=None,
                                        start_time_ut=None,
                                        end_time_ut=None):
    """
    Get a stop-to-stop network describing a single mode of travel.

    Parameters
    ----------
    gtfs : gtfspy.GTFS
    route_type : int
        See gtfspy.route_types.TRANSIT_ROUTE_TYPES for the list of possible types.
    link_attributes: list[str], optional
        defaulting to use the following link attributes:
            "n_vehicles" : Number of vehicles passed
            "duration_min" : minimum travel time between stops
            "duration_max" : maximum travel time between stops
            "duration_median" : median travel time between stops
            "duration_avg" : average travel time between stops
            "d" : distance along straight line (wgs84_distance)
            "distance_shape" : minimum distance along shape
            "capacity_estimate" : approximate capacity passed through the stop
            "route_I_counts" : dict from route_I to counts
    start_time_ut: int
        start time of the time span (in unix time)
    end_time_ut: int
        end time of the time span (in unix time)

    Returns
    -------
    net: networkx.DiGraph
        A directed graph Directed graph
    """
    if link_attributes is None:
        link_attributes = DEFAULT_STOP_TO_STOP_LINK_ATTRIBUTES
    assert(route_type in route_types.TRANSIT_ROUTE_TYPES)

    stops_dataframe = gtfs.get_stops_for_route_type(route_type)
    net = networkx.DiGraph()
    _add_stops_to_net(net, stops_dataframe)

    events_df = gtfs.get_transit_events(start_time_ut=start_time_ut,
                                        end_time_ut=end_time_ut,
                                        route_type=route_type)
    if len(net.nodes()) < 2:
        assert events_df.shape[0] == 0

    # group events by links, and loop over them (i.e. each link):
    link_event_groups = events_df.groupby(['from_stop_I', 'to_stop_I'], sort=False)
    for key, link_events in link_event_groups:
        from_stop_I, to_stop_I = key
        assert isinstance(link_events, pd.DataFrame)
        # 'dep_time_ut' 'arr_time_ut' 'shape_id' 'route_type' 'trip_I' 'duration' 'from_seq' 'to_seq'
        if link_attributes is None:
            net.add_edge(from_stop_I, to_stop_I)
        else:
            link_data = {}
            if "duration_min" in link_attributes:
                link_data['duration_min'] = float(link_events['duration'].min())
            if "duration_max" in link_attributes:
                link_data['duration_max'] = float(link_events['duration'].max())
            if "duration_median" in link_attributes:
                link_data['duration_median'] = float(link_events['duration'].median())
            if "duration_avg" in link_attributes:
                link_data['duration_avg'] = float(link_events['duration'].mean())
            # statistics on numbers of vehicles:
            if "n_vehicles" in link_attributes:
                link_data['n_vehicles'] = int(link_events.shape[0])
            if "capacity_estimate" in link_attributes:
                link_data['capacity_estimate'] = route_types.ROUTE_TYPE_TO_APPROXIMATE_CAPACITY[route_type] \
                                                 * int(link_events.shape[0])
            if "d" in link_attributes:
                from_lat = net.node[from_stop_I]['lat']
                from_lon = net.node[from_stop_I]['lon']
                to_lat = net.node[to_stop_I]['lat']
                to_lon = net.node[to_stop_I]['lon']
                distance = wgs84_distance(from_lat, from_lon, to_lat, to_lon)
                link_data['d'] = int(distance)
            if "distance_shape" in link_attributes:
                assert "shape_id" in link_events.columns.values
                found = None
                for i, shape_id in enumerate(link_events["shape_id"].values):
                    if shape_id is not None:
                        found = i
                        break
                if found is None:
                    link_data["distance_shape"] = None
                else:
                    link_event = link_events.iloc[found]
                    distance = gtfs.get_shape_distance_between_stops(
                        link_event["trip_I"],
                        int(link_event["from_seq"]),
                        int(link_event["to_seq"])
                    )
                    link_data['distance_shape'] = distance
            if "route_I_counts" in link_attributes:
                link_data["route_I_counts"] = link_events.groupby("route_I").size().to_dict()
            net.add_edge(from_stop_I, to_stop_I, attr_dict=link_data)
    return net