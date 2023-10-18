def fetch_official_missions(data_dir, start_date, end_date):
    """
    :param data_dir: (str) directory in which the output file will be saved
    :param start_date: (datetime) first date of the range to be scraped
    :param end_date: (datetime) last date of the range to be scraped
    """
    official_missions = OfficialMissionsDataset()
    df = official_missions.fetch(start_date, end_date)
    save_to_csv(df, data_dir, "official-missions")

    return df