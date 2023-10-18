def pickle_load(path, compression=False):
    """Unpickle a possible compressed pickle.

    Parameters
    ----------
    path: str
        path to the output file
    compression: bool
        if true assumes that pickle was compressed when created and attempts decompression.

    Returns
    -------
    obj: object
        the unpickled object
    """

    if compression:
        with zipfile.ZipFile(path, "r", compression=zipfile.ZIP_DEFLATED) as myzip:
            with myzip.open("data") as f:
                return pickle.load(f)
    else:
        with open(path, "rb") as f:
            return pickle.load(f)