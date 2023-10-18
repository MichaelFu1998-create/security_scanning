def extract_from_array(in_raster=None, in_affine=None, out_tile=None):
    """
    Extract raster data window array.

    Parameters
    ----------
    in_raster : array or ReferencedRaster
    in_affine : ``Affine`` required if in_raster is an array
    out_tile : ``BufferedTile``

    Returns
    -------
    extracted array : array
    """
    if isinstance(in_raster, ReferencedRaster):
        in_affine = in_raster.affine
        in_raster = in_raster.data

    # get range within array
    minrow, maxrow, mincol, maxcol = bounds_to_ranges(
        out_bounds=out_tile.bounds, in_affine=in_affine, in_shape=in_raster.shape
    )
    # if output window is within input window
    if (
        minrow >= 0 and
        mincol >= 0 and
        maxrow <= in_raster.shape[-2] and
        maxcol <= in_raster.shape[-1]
    ):
        return in_raster[..., minrow:maxrow, mincol:maxcol]
    # raise error if output is not fully within input
    else:
        raise ValueError("extraction fails if output shape is not within input")