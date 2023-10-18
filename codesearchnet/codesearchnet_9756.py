def _add_stops_to_net(net, stops):
    """
    Add nodes to the network from the pandas dataframe describing (a part of the) stops table in the GTFS database.

    Parameters
    ----------
    net: networkx.Graph
    stops: pandas.DataFrame
    """
    for stop in stops.itertuples():
        data = {
            "lat": stop.lat,
            "lon": stop.lon,
            "name": stop.name
        }
        net.add_node(stop.stop_I, data)