def source_csv_to_pandas(path, table, read_csv_args=None):
    """
    Parameters
    ----------
    path: str
        path to directory or zipfile
    table: str
        name of table
    read_csv_args:
        string arguments passed to the read_csv function

    Returns
    -------
    df: pandas:DataFrame
    """
    if '.txt' not in table:
        table += '.txt'

    if isinstance(path, dict):
        data_obj = path[table]
        f = data_obj.split("\n")
    else:
        if os.path.isdir(path):
            f = open(os.path.join(path, table))

        else:

            z = zipfile.ZipFile(path)
            for path in z.namelist():
                if table in path:
                    table = path
                    break
            try:
                f = zip_open(z, table)
            except KeyError as e:
                return pd.DataFrame()

    if read_csv_args:
        df = pd.read_csv(**read_csv_args)
    else:
        df = pd.read_csv(f)
    return df