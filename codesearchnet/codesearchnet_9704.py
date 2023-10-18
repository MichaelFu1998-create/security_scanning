def write_combined_transit_stop_to_stop_network(gtfs, output_path, fmt=None):
    """
    Parameters
    ----------
    gtfs : gtfspy.GTFS
    output_path : str
    fmt: None, optional
        defaulting to "edg" and writing results as ".edg" files
         If "csv" csv files are produced instead    """
    if fmt is None:
        fmt = "edg"
    multi_di_graph = combined_stop_to_stop_transit_network(gtfs)
    _write_stop_to_stop_network_edges(multi_di_graph, output_path, fmt=fmt)