def route_to_route_network(gtfs, walking_threshold, start_time, end_time):
    """
    Creates networkx graph where the nodes are bus routes and a edge indicates that there is a possibility to transfer
    between the routes
    :param gtfs:
    :param walking_threshold:
    :param start_time:
    :param end_time:
    :return:
    """
    graph = networkx.Graph()
    routes = gtfs.get_table("routes")

    for i in routes.itertuples():
        graph.add_node(i.route_id, attr_dict={"type": i.type, "color": route_types.ROUTE_TYPE_TO_COLOR[i.type]})


    query = """SELECT stop1.route_id AS route_id1, stop1.type, stop2.route_id AS route_id2, stop2.type FROM
                (SELECT * FROM stop_distances WHERE d_walk < %s) sd,
                (SELECT * FROM stop_times, trips, routes 
                WHERE stop_times.trip_I=trips.trip_I AND trips.route_I=routes.route_I 
                AND stop_times.dep_time_ds > %s AND stop_times.dep_time_ds < %s) stop1,
                (SELECT * FROM stop_times, trips, routes 
                WHERE stop_times.trip_I=trips.trip_I AND trips.route_I=routes.route_I 
                AND stop_times.dep_time_ds > %s AND stop_times.dep_time_ds < %s) stop2
                WHERE sd.from_stop_I = stop1.stop_I AND sd.to_stop_I = stop2.stop_I AND stop1.route_id != stop2.route_id
                GROUP BY stop1.route_id, stop2.route_id""" % (walking_threshold, start_time, end_time, start_time,
                                                              end_time)
    df = gtfs.execute_custom_query_pandas(query)

    for items in df.itertuples():
        graph.add_edge(items.route_id1, items.route_id2)
    graph.remove_nodes_from(networkx.isolates(graph))
    return graph