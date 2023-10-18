def calculate_slope_aspect(elevation, xres, yres, z=1.0, scale=1.0):
    """
    Calculate slope and aspect map.

    Return a pair of arrays 2 pixels smaller than the input elevation array.

    Slope is returned in radians, from 0 for sheer face to pi/2 for
    flat ground. Aspect is returned in radians, counterclockwise from -pi
    at north around to pi.

    Logic here is borrowed from hillshade.cpp:
    http://www.perrygeo.net/wordpress/?p=7

    Parameters
    ----------
    elevation : array
        input elevation data
    xres : float
        column width
    yres : float
        row  height
    z : float
        vertical exaggeration factor
    scale : float
        scale factor of pixel size units versus height units (insert 112000
        when having elevation values in meters in a geodetic projection)

    Returns
    -------
    slope shade : array
    """
    z = float(z)
    scale = float(scale)
    height, width = elevation.shape[0] - 2, elevation.shape[1] - 2
    window = [
        z * elevation[row:(row + height), col:(col + width)]
        for (row, col) in product(range(3), range(3))
    ]
    x = (
        (window[0] + window[3] + window[3] + window[6])
        - (window[2] + window[5] + window[5] + window[8])
        ) / (8.0 * xres * scale)
    y = (
        (window[6] + window[7] + window[7] + window[8])
        - (window[0] + window[1] + window[1] + window[2])
        ) / (8.0 * yres * scale)
    # in radians, from 0 to pi/2
    slope = math.pi/2 - np.arctan(np.sqrt(x*x + y*y))
    # in radians counterclockwise, from -pi at north back to pi
    aspect = np.arctan2(x, y)
    return slope, aspect