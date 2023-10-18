def fetch_speeches(data_dir, range_start, range_end):
    """
    :param data_dir: (str) directory in which the output file will be saved
    :param range_start: (str) date in the format dd/mm/yyyy
    :param range_end: (str) date in the format dd/mm/yyyy
    """
    speeches = SpeechesDataset()
    df = speeches.fetch(range_start, range_end)
    save_to_csv(df, data_dir, "speeches")
    return df