def write_static_networks(gtfs, output_dir, fmt=None):
    """
    Parameters
    ----------
    gtfs: gtfspy.GTFS
    output_dir: (str, unicode)
        a path where to write
    fmt: None, optional
        defaulting to "edg" and writing results as ".edg" files
         If "csv" csv files are produced instead
    """
    if fmt is None:
        fmt = "edg"
    single_layer_networks = stop_to_stop_networks_by_type(gtfs)
    util.makedirs(output_dir)
    for route_type, net in single_layer_networks.items():
        tag = route_types.ROUTE_TYPE_TO_LOWERCASE_TAG[route_type]
        file_name = os.path.join(output_dir, "network_" + tag + "." + fmt)
        if len(net.edges()) > 0:
            _write_stop_to_stop_network_edges(net, file_name, fmt=fmt)