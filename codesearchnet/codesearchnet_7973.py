def fetch_presences(data_dir, deputies, date_start, date_end):
    """
    :param data_dir: (str) directory in which the output file will be saved
    :param deputies: (pandas.DataFrame) a dataframe with deputies data
    :param date_start: (str) a date in the format dd/mm/yyyy
    :param date_end: (str) a date in the format dd/mm/yyyy
    """
    presences = PresencesDataset()
    df = presences.fetch(deputies, date_start, date_end)
    save_to_csv(df, data_dir, "presences")

    log.info("Presence records:", len(df))
    log.info("Records of deputies present on a session:", len(df[df.presence == 'Present']))
    log.info("Records of deputies absent from a session:", len(df[df.presence == 'Absent']))

    return df