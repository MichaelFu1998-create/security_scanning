def add_walk_distances_to_db_python(gtfs, osm_path, cutoff_distance_m=1000):
    """
    Computes the walk paths between stops, and updates these to the gtfs database.

    Parameters
    ----------
    gtfs: gtfspy.GTFS or str
        A GTFS object or a string representation.
    osm_path: str
        path to the OpenStreetMap file
    cutoff_distance_m: number
        maximum allowed distance in meters

    Returns
    -------
    None

    See Also
    --------
    gtfspy.calc_transfers
    compute_walk_paths_java
    """
    if isinstance(gtfs, str):
        gtfs = GTFS(gtfs)
    assert (isinstance(gtfs, GTFS))
    print("Reading in walk network")
    walk_network = create_walk_network_from_osm(osm_path)
    print("Matching stops to the OSM network")
    stop_I_to_nearest_osm_node, stop_I_to_nearest_osm_node_distance = match_stops_to_nodes(gtfs, walk_network)

    transfers = gtfs.get_straight_line_transfer_distances()

    from_I_to_to_stop_Is = {stop_I: set() for stop_I in stop_I_to_nearest_osm_node}
    for transfer_tuple in transfers.itertuples():
        from_I = transfer_tuple.from_stop_I
        to_I = transfer_tuple.to_stop_I
        from_I_to_to_stop_Is[from_I].add(to_I)

    print("Computing walking distances")
    for from_I, to_stop_Is in from_I_to_to_stop_Is.items():
        from_node = stop_I_to_nearest_osm_node[from_I]
        from_dist = stop_I_to_nearest_osm_node_distance[from_I]
        shortest_paths = networkx.single_source_dijkstra_path_length(walk_network,
                                                                     from_node,
                                                                     cutoff=cutoff_distance_m - from_dist,
                                                                     weight="distance")
        for to_I in to_stop_Is:
            to_distance = stop_I_to_nearest_osm_node_distance[to_I]
            to_node = stop_I_to_nearest_osm_node[to_I]
            osm_distance = shortest_paths.get(to_node, float('inf'))
            total_distance = from_dist + osm_distance + to_distance
            from_stop_I_transfers = transfers[transfers['from_stop_I'] == from_I]
            straigth_distance = from_stop_I_transfers[from_stop_I_transfers["to_stop_I"] == to_I]["d"].values[0]
            assert (straigth_distance < total_distance + 2)  # allow for a maximum  of 2 meters in calculations
            if total_distance <= cutoff_distance_m:
                gtfs.conn.execute("UPDATE stop_distances "
                                  "SET d_walk = " + str(int(total_distance)) +
                                  " WHERE from_stop_I=" + str(from_I) + " AND to_stop_I=" + str(to_I))

    gtfs.conn.commit()