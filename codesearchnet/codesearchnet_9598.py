def hillshade(elevation, tile, azimuth=315.0, altitude=45.0, z=1.0, scale=1.0):
    """
    Return hillshaded numpy array.

    Parameters
    ----------
    elevation : array
        input elevation data
    tile : Tile
        tile covering the array
    z : float
        vertical exaggeration factor
    scale : float
        scale factor of pixel size units versus height units (insert 112000
        when having elevation values in meters in a geodetic projection)
    """
    azimuth = float(azimuth)
    altitude = float(altitude)
    z = float(z)
    scale = float(scale)
    xres = tile.tile.pixel_x_size
    yres = -tile.tile.pixel_y_size
    slope, aspect = calculate_slope_aspect(
        elevation, xres, yres, z=z, scale=scale)
    deg2rad = math.pi / 180.0
    shaded = np.sin(altitude * deg2rad) * np.sin(slope) \
        + np.cos(altitude * deg2rad) * np.cos(slope) \
        * np.cos((azimuth - 90.0) * deg2rad - aspect)
    # shaded now has values between -1.0 and +1.0
    # stretch to 0 - 255 and invert
    shaded = (((shaded+1.0)/2)*-255.0).astype("uint8")
    # add one pixel padding using the edge values
    return ma.masked_array(
        data=np.pad(shaded, 1, mode='edge'), mask=elevation.mask
    )