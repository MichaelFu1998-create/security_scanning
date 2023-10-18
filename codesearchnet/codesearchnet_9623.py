def read_raster_window(
    input_files,
    tile,
    indexes=None,
    resampling="nearest",
    src_nodata=None,
    dst_nodata=None,
    gdal_opts=None
):
    """
    Return NumPy arrays from an input raster.

    NumPy arrays are reprojected and resampled to tile properties from input
    raster. If tile boundaries cross the antimeridian, data on the other side
    of the antimeridian will be read and concatenated to the numpy array
    accordingly.

    Parameters
    ----------
    input_files : string or list
        path to a raster file or list of paths to multiple raster files readable by
        rasterio.
    tile : Tile
        a Tile object
    indexes : list or int
        a list of band numbers; None will read all.
    resampling : string
        one of "nearest", "average", "bilinear" or "lanczos"
    src_nodata : int or float, optional
        if not set, the nodata value from the source dataset will be used
    dst_nodata : int or float, optional
        if not set, the nodata value from the source dataset will be used
    gdal_opts : dict
        GDAL options passed on to rasterio.Env()

    Returns
    -------
    raster : MaskedArray
    """
    with rasterio.Env(
        **get_gdal_options(
            gdal_opts,
            is_remote=path_is_remote(
                input_files[0] if isinstance(input_files, list) else input_files, s3=True
            )
        )
    ) as env:
        logger.debug("reading %s with GDAL options %s", input_files, env.options)
        return _read_raster_window(
            input_files,
            tile,
            indexes=indexes,
            resampling=resampling,
            src_nodata=src_nodata,
            dst_nodata=dst_nodata
        )