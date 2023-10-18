def table(cluster):
    """
    Create a numpy.ndarray with all observed fields and
    computed teff and luminosity values.
    """
    teffs = teff(cluster)
    lums = luminosity(cluster)
    arr = cluster.to_array()
    i = 0
    for row in arr:
        row['lum'][0] = np.array([lums[i]], dtype='f')
        row['temp'][0] = np.array([teffs[i]], dtype='f')
        i += 1
    arr = round_arr_teff_luminosity(arr)
    return arr