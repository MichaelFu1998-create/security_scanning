def combined_stop_to_stop_transit_network(gtfs, start_time_ut=None, end_time_ut=None):
    """
    Compute stop-to-stop networks for all travel modes and combine them into a single network.
    The modes of transport are encoded to a single network.
    The network consists of multiple links corresponding to each travel mode.
    Walk mode is not included.

    Parameters
    ----------
    gtfs: gtfspy.GTFS

    Returns
    -------
    net: networkx.MultiDiGraph
        keys should be one of route_types.TRANSIT_ROUTE_TYPES (i.e. GTFS route_types)
    """
    multi_di_graph = networkx.MultiDiGraph()
    for route_type in route_types.TRANSIT_ROUTE_TYPES:
        graph = stop_to_stop_network_for_route_type(gtfs, route_type,
                                                    start_time_ut=start_time_ut, end_time_ut=end_time_ut)
        for from_node, to_node, data in graph.edges(data=True):
            data['route_type'] = route_type
        multi_di_graph.add_edges_from(graph.edges(data=True))
        multi_di_graph.add_nodes_from(graph.nodes(data=True))
    return multi_di_graph