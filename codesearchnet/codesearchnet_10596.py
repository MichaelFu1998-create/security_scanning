def extracted_array_2d_from_array_2d_and_coordinates(array_2d, y0, y1, x0, x1):
    """Resize an array to a new size by extracting a sub-set of the array.

    The extracted input coordinates use NumPy convention, such that the upper values should be specified as +1 the \
    dimensions of the extracted array.

    In the example below, an array of size (5,5) is extracted using the coordinates y0=1, y1=4, x0=1, x1=4. This
    extracts an array of dimensions (2,2) and is equivalent to array_2d[1:4, 1:4]

    Parameters
    ----------
    array_2d : ndarray
        The 2D array that is an array is extracted from.
    y0 : int
        The lower row number (e.g. the higher y-coodinate) of the array that is extracted for the resize.
    y1 : int
        The upper row number (e.g. the lower y-coodinate) of the array that is extracted for the resize.
    x0 : int
        The lower column number (e.g. the lower x-coodinate) of the array that is extracted for the resize.
    x1 : int
        The upper column number (e.g. the higher x-coodinate) of the array that is extracted for the resize.

    Returns
    -------
    ndarray
        The extracted 2D array from the input 2D array.

    Examples
    --------
    array_2d = np.ones((5,5))
    extracted_array = extract_array_2d(array_2d=array_2d, y0=1, y1=4, x0=1, x1=4)
    """

    new_shape = (y1-y0, x1-x0)

    resized_array = np.zeros(shape=new_shape)

    for y_resized, y in enumerate(range(y0, y1)):
        for x_resized, x in enumerate(range(x0, x1)):
                resized_array[y_resized, x_resized] = array_2d[y, x]

    return resized_array