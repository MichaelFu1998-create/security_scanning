def write_gtfs(gtfs, output):
    """
    Write out the database according to the GTFS format.

    Parameters
    ----------
    gtfs: gtfspy.GTFS
    output: str
        Path where to put the GTFS files
        if output ends with ".zip" a ZIP-file is created instead.

    Returns
    -------
    None
    """
    output = os.path.abspath(output)
    uuid_str = "tmp_" + str(uuid.uuid1())
    if output[-4:] == '.zip':
        zip = True
        out_basepath = os.path.dirname(os.path.abspath(output))
        if not os.path.exists(out_basepath):
            raise IOError(out_basepath + " does not exist, cannot write gtfs as a zip")
        tmp_dir = os.path.join(out_basepath, str(uuid_str))
        # zip_file_na,e = ../out_basedir + ".zip
    else:
        zip = False
        out_basepath = output
        tmp_dir = os.path.join(out_basepath + "_" + str(uuid_str))

    os.makedirs(tmp_dir, exist_ok=True)

    gtfs_table_to_writer = {
        "agency": _write_gtfs_agencies,
        "calendar": _write_gtfs_calendar,
        "calendar_dates": _write_gtfs_calendar_dates,
        # fare attributes and fare_rules omitted (seldomly used)
        "feed_info": _write_gtfs_feed_info,
        # "frequencies": not written, as they are incorporated into trips and routes,
        # Frequencies table is expanded into other tables on initial import. -> Thus frequencies.txt is not created
        "routes": _write_gtfs_routes,
        "shapes": _write_gtfs_shapes,
        "stops": _write_gtfs_stops,
        "stop_times": _write_gtfs_stop_times,
        "transfers": _write_gtfs_transfers,
        "trips": _write_gtfs_trips,
    }

    for table, writer in gtfs_table_to_writer.items():
        fname_to_write = os.path.join(tmp_dir, table + '.txt')
        print(fname_to_write)
        writer(gtfs, open(os.path.join(tmp_dir, table + '.txt'), 'w'))

    if zip:
        shutil.make_archive(output[:-4], 'zip', tmp_dir)
        shutil.rmtree(tmp_dir)
    else:
        print("moving " + str(tmp_dir) + " to " + out_basepath)
        os.rename(tmp_dir, out_basepath)