def round_arr_teff_luminosity(arr):
    """
    Return the numpy array with rounded teff and luminosity columns.
    """
    arr['temp'] = np.around(arr['temp'], -1)
    arr['lum'] = np.around(arr['lum'], 3)
    return arr