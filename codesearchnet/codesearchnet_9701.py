def write_walk_transfer_edges(gtfs, output_file_name):
    """
    Parameters
    ----------
    gtfs: gtfspy.GTFS
    output_file_name: str
    """
    transfers = gtfs.get_table("stop_distances")
    transfers.drop([u"min_transfer_time", u"timed_transfer"], 1, inplace=True)
    with util.create_file(output_file_name, tmpdir=True, keepext=True) as tmpfile:
        transfers.to_csv(tmpfile, encoding='utf-8', index=False)