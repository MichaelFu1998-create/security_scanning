def map_2d_indexes_to_1d_indexes_for_shape(indexes_2d, shape):
    """For pixels on a 2D array of shape (rows, colums), map an array of 2D pixel indexes to 1D pixel indexes.

    Indexing is defined from the top-left corner rightwards and downwards, whereby the top-left pixel on the 2D array
    corresponds to index 0, the pixel to its right pixel 1, and so on.

    For a 2D array of shape (3,3), 2D pixel indexes are converted as follows:

    - 2D Pixel index [0,0] maps -> 1D pixel index 0.
    - 2D Pixel index [0,1] maps -> 2D pixel index 1.
    - 2D Pixel index [1,0] maps -> 2D pixel index 4.
    - 2D Pixel index [2,2] maps -> 2D pixel index 8.

    Parameters
     ----------
    indexes_2d : ndarray
        The 2D pixel indexes which are mapped to 1D indexes.
    shape : (int, int)
        The shape of the 2D array which the pixels are defined on.

    Returns
    --------
    ndarray
        An array of 1d pixel indexes with dimensions (total_indexes).

    Examples
    --------
    indexes_2d = np.array([[0,0], [1,0], [2,0], [2,2]])
    indexes_1d = map_1d_indexes_to_1d_indexes_for_shape(indexes_2d=indexes_2d, shape=(3,3))
    """
    indexes_1d = np.zeros(indexes_2d.shape[0])

    for i in range(indexes_2d.shape[0]):
        indexes_1d[i] = int((indexes_2d[i, 0]) * shape[1] + indexes_2d[i, 1])

    return indexes_1d