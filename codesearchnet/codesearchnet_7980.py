def fetch_deputies(data_dir):
    """
    :param data_dir: (str) directory in which the output file will be saved
    """
    deputies = DeputiesDataset()
    df = deputies.fetch()
    save_to_csv(df, data_dir, "deputies")

    holders = df.condition == 'Holder'
    substitutes = df.condition == 'Substitute'
    log.info("Total deputies:", len(df))
    log.info("Holder deputies:", len(df[holders]))
    log.info("Substitute deputies:", len(df[substitutes]))
    return df