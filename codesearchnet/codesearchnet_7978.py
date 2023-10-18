def fetch_session_start_times(data_dir, pivot, session_dates):
    """
    :param data_dir: (str) directory in which the output file will be saved
    :param pivot: (int) congressperson document to use as a pivot for scraping the data
    :param session_dates: (list) datetime objects to fetch the start times for
    """
    session_start_times = SessionStartTimesDataset()
    df = session_start_times.fetch(pivot, session_dates)
    save_to_csv(df, data_dir, "session-start-times")

    log.info("Dates requested:", len(session_dates))
    found = pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M:%S").dt.date.unique()
    log.info("Dates found:", len(found))
    return df