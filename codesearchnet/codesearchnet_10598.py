def bin_up_array_2d_using_mean(array_2d, bin_up_factor):
    """Bin up an array to coarser resolution, by binning up groups of pixels and using their mean value to determine \
     the value of the new pixel.

    If an array of shape (8,8) is input and the bin up size is 2, this would return a new array of size (4,4) where \
    every pixel was the mean of each collection of 2x2 pixels on the (8,8) array.

    If binning up the array leads to an edge being cut (e.g. a (9,9) array binned up by 2), an array is first \
    extracted around the centre of that array.


    Parameters
    ----------
    array_2d : ndarray
        The 2D array that is resized.
    new_shape : (int, int)
        The (y,x) new pixel dimension of the trimmed array.
    origin : (int, int)
        The oigin of the resized array, e.g. the central pixel around which the array is extracted.

    Returns
    -------
    ndarray
        The resized 2D array from the input 2D array.

    Examples
    --------
    array_2d = np.ones((5,5))
    resize_array = resize_array_2d(array_2d=array_2d, new_shape=(2,2), origin=(2, 2))
    """

    padded_array_2d = pad_2d_array_for_binning_up_with_bin_up_factor(array_2d=array_2d, bin_up_factor=bin_up_factor)

    binned_array_2d = np.zeros(shape=(padded_array_2d.shape[0] // bin_up_factor,
                                      padded_array_2d.shape[1] // bin_up_factor))

    for y in range(binned_array_2d.shape[0]):
        for x in range(binned_array_2d.shape[1]):
            value = 0.0
            for y1 in range(bin_up_factor):
                for x1 in range(bin_up_factor):
                    padded_y = y*bin_up_factor + y1
                    padded_x = x*bin_up_factor + x1
                    value += padded_array_2d[padded_y, padded_x]

            binned_array_2d[y,x] = value / (bin_up_factor ** 2.0)

    return binned_array_2d