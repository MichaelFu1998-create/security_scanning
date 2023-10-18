def bounds_to_ranges(out_bounds=None, in_affine=None, in_shape=None):
    """
    Return bounds range values from geolocated input.

    Parameters
    ----------
    out_bounds : tuple
        left, bottom, right, top
    in_affine : Affine
        input geolocation
    in_shape : tuple
        input shape

    Returns
    -------
    minrow, maxrow, mincol, maxcol
    """
    return itertools.chain(
        *from_bounds(
            *out_bounds, transform=in_affine, height=in_shape[-2], width=in_shape[-1]
        ).round_lengths(pixel_precision=0).round_offsets(pixel_precision=0).toranges()
    )