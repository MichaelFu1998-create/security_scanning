def preprocessing_br_projection_excel(path: str) -> pd.DataFrame:
    """Preprocess the excel file.

    Parameters
    ----------
    path : Filepath of the excel sheet
    """
    if not os.path.exists(path):
        raise ValueError("Error: %s file not found" % path)

    return pd.read_excel(path, sheetname=0, header=0)