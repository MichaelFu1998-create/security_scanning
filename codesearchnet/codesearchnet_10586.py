def map_1d_indexes_to_2d_indexes_for_shape(indexes_1d, shape):
    """For pixels on a 2D array of shape (rows, colums), map an array of 1D pixel indexes to 2D pixel indexes.

    Indexing is defined from the top-left corner rightwards and downwards, whereby the top-left pixel on the 2D array
    corresponds to index 0, the pixel to its right pixel 1, and so on.

    For a 2D array of shape (3,3), 1D pixel indexes are converted as follows:

    - 1D Pixel index 0 maps -> 2D pixel index [0,0].
    - 1D Pixel index 1 maps -> 2D pixel index [0,1].
    - 1D Pixel index 4 maps -> 2D pixel index [1,0].
    - 1D Pixel index 8 maps -> 2D pixel index [2,2].

    Parameters
     ----------
    indexes_1d : ndarray
        The 1D pixel indexes which are mapped to 2D indexes.
    shape : (int, int)
        The shape of the 2D array which the pixels are defined on.

    Returns
    --------
    ndarray
        An array of 2d pixel indexes with dimensions (total_indexes, 2).

    Examples
    --------
    indexes_1d = np.array([0, 1, 2, 5])
    indexes_2d = map_1d_indexes_to_2d_indexes_for_shape(indexes_1d=indexes_1d, shape=(3,3))
    """
    indexes_2d = np.zeros((indexes_1d.shape[0], 2))

    for i, index_1d in enumerate(indexes_1d):
        indexes_2d[i, 0] = int(index_1d / shape[1])
        indexes_2d[i, 1] = int(index_1d % shape[1])

    return indexes_2d