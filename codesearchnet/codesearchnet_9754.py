def stop_to_stop_networks_by_type(gtfs):
    """
    Compute stop-to-stop networks for all travel modes (route_types).

    Parameters
    ----------
    gtfs: gtfspy.GTFS

    Returns
    -------
    dict: dict[int, networkx.DiGraph]
        keys should be one of route_types.ALL_ROUTE_TYPES (i.e. GTFS route_types)
    """
    route_type_to_network = dict()
    for route_type in route_types.ALL_ROUTE_TYPES:
        if route_type == route_types.WALK:
            net = walk_transfer_stop_to_stop_network(gtfs)
        else:
            net = stop_to_stop_network_for_route_type(gtfs, route_type)
        route_type_to_network[route_type] = net
    assert len(route_type_to_network) == len(route_types.ALL_ROUTE_TYPES)
    return route_type_to_network