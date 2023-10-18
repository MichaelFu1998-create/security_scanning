def write_temporal_network(gtfs, output_filename, start_time_ut=None, end_time_ut=None):
    """
    Parameters
    ----------
    gtfs : gtfspy.GTFS
    output_filename : str
        path to the directory where to store the extracts
    start_time_ut: int | None
        start time of the extract in unixtime (seconds after epoch)
    end_time_ut: int | None
        end time of the extract in unixtime (seconds after epoch)
    """
    util.makedirs(os.path.dirname(os.path.abspath(output_filename)))
    pandas_data_frame = temporal_network(gtfs, start_time_ut=start_time_ut, end_time_ut=end_time_ut)
    pandas_data_frame.to_csv(output_filename, encoding='utf-8', index=False)