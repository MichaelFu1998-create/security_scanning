def match_stops_to_nodes(gtfs, walk_network):
    """
    Parameters
    ----------
    gtfs : a GTFS object
    walk_network : networkx.Graph

    Returns
    -------
    stop_I_to_node: dict
        maps stop_I to closest walk_network node
    stop_I_to_dist: dict
        maps stop_I to the distance to the closest walk_network node
    """
    network_nodes = walk_network.nodes(data="true")

    stop_Is = set(gtfs.get_straight_line_transfer_distances()['from_stop_I'])
    stops_df = gtfs.stops()

    geo_index = GeoGridIndex(precision=6)
    for net_node, data in network_nodes:
        geo_index.add_point(GeoPoint(data['lat'], data['lon'], ref=net_node))
    stop_I_to_node = {}
    stop_I_to_dist = {}
    for stop_I in stop_Is:
        stop_lat = float(stops_df[stops_df.stop_I == stop_I].lat)
        stop_lon = float(stops_df[stops_df.stop_I == stop_I].lon)
        geo_point = GeoPoint(stop_lat, stop_lon)
        min_dist = float('inf')
        min_dist_node = None
        search_distances_m = [0.100, 0.500]
        for search_distance_m in search_distances_m:
            for point, distance in geo_index.get_nearest_points(geo_point, search_distance_m, "km"):
                if distance < min_dist:
                    min_dist = distance * 1000
                    min_dist_node = point.ref
            if min_dist_node is not None:
                break
        if min_dist_node is None:
            warn("No OSM node found for stop: " + str(stops_df[stops_df.stop_I == stop_I]))
        stop_I_to_node[stop_I] = min_dist_node
        stop_I_to_dist[stop_I] = min_dist
    return stop_I_to_node, stop_I_to_dist