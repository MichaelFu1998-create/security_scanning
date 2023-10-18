def read_vector_window(input_files, tile, validity_check=True):
    """
    Read a window of an input vector dataset.

    Also clips geometry.

    Parameters:
    -----------
    input_file : string
        path to vector file
    tile : ``Tile``
        tile extent to read data from
    validity_check : bool
        checks if reprojected geometry is valid and throws ``RuntimeError`` if
        invalid (default: True)

    Returns
    -------
    features : list
      a list of reprojected GeoJSON-like features
    """
    if not isinstance(input_files, list):
        input_files = [input_files]
    return [
        feature
        for feature in chain.from_iterable([
            _read_vector_window(path, tile, validity_check=validity_check)
            for path in input_files
        ])
    ]