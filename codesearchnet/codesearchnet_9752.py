def walk_transfer_stop_to_stop_network(gtfs, max_link_distance=None):
    """
    Construct the walk network.
    If OpenStreetMap-based walking distances have been computed, then those are used as the distance.
    Otherwise, the great circle distances ("d") is used.

    Parameters
    ----------
    gtfs: gtfspy.GTFS
    max_link_distance: int, optional
        If given, all walking transfers with great circle distance longer
        than this limit (expressed in meters) will be omitted.

    Returns
    -------
    net: networkx.DiGraph
        edges have attributes
            d:
                straight-line distance between stops
            d_walk:
                distance along the road/tracks/..
    """
    if max_link_distance is None:
        max_link_distance = 1000
    net = networkx.Graph()
    _add_stops_to_net(net, gtfs.get_table("stops"))
    stop_distances = gtfs.get_table("stop_distances")
    if stop_distances["d_walk"][0] is None:
        osm_distances_available = False
        warn("Warning: OpenStreetMap-based walking distances have not been computed, using euclidean distances instead."
             "Ignore this warning if running unit tests.")
    else:
        osm_distances_available = True

    for stop_distance_tuple in stop_distances.itertuples():
        from_node = stop_distance_tuple.from_stop_I
        to_node = stop_distance_tuple.to_stop_I

        if osm_distances_available:
            if stop_distance_tuple.d_walk > max_link_distance or isnan(stop_distance_tuple.d_walk):
                continue
            data = {'d': stop_distance_tuple.d, 'd_walk': stop_distance_tuple.d_walk}
        else:
            if stop_distance_tuple.d > max_link_distance:
                continue
            data = {'d': stop_distance_tuple.d}
        net.add_edge(from_node, to_node, data)
    return net