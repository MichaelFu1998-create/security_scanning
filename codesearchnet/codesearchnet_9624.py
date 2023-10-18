def _get_warped_array(
    input_file=None,
    indexes=None,
    dst_bounds=None,
    dst_shape=None,
    dst_crs=None,
    resampling=None,
    src_nodata=None,
    dst_nodata=None
):
    """Extract a numpy array from a raster file."""
    try:
        return _rasterio_read(
            input_file=input_file,
            indexes=indexes,
            dst_bounds=dst_bounds,
            dst_shape=dst_shape,
            dst_crs=dst_crs,
            resampling=resampling,
            src_nodata=src_nodata,
            dst_nodata=dst_nodata
        )
    except Exception as e:
        logger.exception("error while reading file %s: %s", input_file, e)
        raise