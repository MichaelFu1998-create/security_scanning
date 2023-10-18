def write_stops_geojson(gtfs, out_file, fields=None):
    """
    Parameters
    ----------
    gtfs: gtfspy.GTFS
    out_file: file-like or path to file
    fields: dict
        simultaneously map each original_name to the new_name
    Returns
    -------
    """
    geojson = create_stops_geojson_dict(gtfs, fields)
    if hasattr(out_file, "write"):
        out_file.write(json.dumps(geojson))
    else:
        with util.create_file(out_file, tmpdir=True, keepext=True) as tmpfile_path:
            tmpfile = open(tmpfile_path, 'w')
            tmpfile.write(json.dumps(geojson))