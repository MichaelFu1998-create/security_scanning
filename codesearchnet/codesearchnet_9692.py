def get_walk_network(gtfs, max_link_distance_m=1000):
    """
    Parameters
    ----------
    gtfs: gtfspy.GTFS

    Returns
    -------
    walk_network: networkx.Graph:
    """
    assert (isinstance(gtfs, GTFS))
    return walk_transfer_stop_to_stop_network(gtfs, max_link_distance=max_link_distance_m)