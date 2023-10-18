def write_stats_as_csv(gtfs, path_to_csv, re_write=False):
    """
    Writes data from get_stats to csv file

    Parameters
    ----------
    gtfs: GTFS
    path_to_csv: str
        filepath to the csv file to be generated
    re_write:
        insted of appending, create a new one.
    """
    stats_dict = get_stats(gtfs)
    # check if file exist
    if re_write:
            os.remove(path_to_csv)
    
    #if not os.path.isfile(path_to_csv):
     #   is_new = True
    #else:
     #   is_new = False
    
    is_new = True
    mode = 'r' if os.path.exists(path_to_csv) else 'w+'
    with open(path_to_csv, mode) as csvfile:
        for line in csvfile:
           if line:
               is_new = False
           else:
               is_new = True

    with open(path_to_csv, 'a') as csvfile:
        if (sys.version_info > (3, 0)):
            delimiter = u","
        else:
            delimiter = b","
        statswriter = csv.writer(csvfile, delimiter=delimiter)
        # write column names if
        if is_new:
            statswriter.writerow([key for key in sorted(stats_dict.keys())])

        row_to_write = []
        # write stats row sorted by column name
        for key in sorted(stats_dict.keys()):
            row_to_write.append(stats_dict[key])
        statswriter.writerow(row_to_write)