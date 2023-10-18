def file_modified_time(file_name) -> pd.Timestamp:
    """
    File modified time in python

    Args:
        file_name: file name

    Returns:
        pd.Timestamp
    """
    return pd.to_datetime(time.ctime(os.path.getmtime(filename=file_name)))