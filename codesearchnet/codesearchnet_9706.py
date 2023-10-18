def write_temporal_networks_by_route_type(gtfs, extract_output_dir):
    """
    Write temporal networks by route type to disk.

    Parameters
    ----------
    gtfs: gtfspy.GTFS
    extract_output_dir: str
    """
    util.makedirs(extract_output_dir)
    for route_type in route_types.TRANSIT_ROUTE_TYPES:
        pandas_data_frame = temporal_network(gtfs, start_time_ut=None, end_time_ut=None, route_type=route_type)
        tag = route_types.ROUTE_TYPE_TO_LOWERCASE_TAG[route_type]
        out_file_name = os.path.join(extract_output_dir, tag + ".tnet")
        pandas_data_frame.to_csv(out_file_name, encoding='utf-8', index=False)