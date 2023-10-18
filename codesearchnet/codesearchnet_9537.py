def pyramid(
    input_raster,
    output_dir,
    pyramid_type=None,
    output_format=None,
    resampling_method=None,
    scale_method=None,
    zoom=None,
    bounds=None,
    overwrite=False,
    debug=False
):
    """Create tile pyramid out of input raster."""
    bounds = bounds if bounds else None
    options = dict(
        pyramid_type=pyramid_type,
        scale_method=scale_method,
        output_format=output_format,
        resampling=resampling_method,
        zoom=zoom,
        bounds=bounds,
        overwrite=overwrite
    )
    raster2pyramid(input_raster, output_dir, options)