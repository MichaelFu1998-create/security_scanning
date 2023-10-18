def write_nodes(gtfs, output, fields=None):
    """
    Parameters
    ----------
    gtfs: gtfspy.GTFS
    output: str
        Path to the output file
    fields: list, optional
        which pieces of information to provide
    """
    nodes = gtfs.get_table("stops")
    if fields is not None:
        nodes = nodes[fields]
    with util.create_file(output, tmpdir=True, keepext=True) as tmpfile:
        nodes.to_csv(tmpfile, encoding='utf-8', index=False, sep=";")