def raster2pyramid(input_file, output_dir, options):
    """Create a tile pyramid out of an input raster dataset."""
    pyramid_type = options["pyramid_type"]
    scale_method = options["scale_method"]
    output_format = options["output_format"]
    resampling = options["resampling"]
    zoom = options["zoom"]
    bounds = options["bounds"]
    mode = "overwrite" if options["overwrite"] else "continue"

    # Prepare process parameters
    minzoom, maxzoom = _get_zoom(zoom, input_file, pyramid_type)
    with rasterio.open(input_file, "r") as input_raster:
        output_bands = input_raster.count
        input_dtype = input_raster.dtypes[0]
        output_dtype = input_raster.dtypes[0]
        nodataval = input_raster.nodatavals[0]
        nodataval = nodataval if nodataval else 0
        if output_format == "PNG" and output_bands > 3:
            output_bands = 3
            output_dtype = 'uint8'
        scales_minmax = ()
        if scale_method == "dtype_scale":
            for index in range(1, output_bands+1):
                scales_minmax += (DTYPE_RANGES[input_dtype], )
        elif scale_method == "minmax_scale":
            for index in range(1, output_bands+1):
                band = input_raster.read(index)
                scales_minmax += ((band.min(), band.max()), )
        elif scale_method == "crop":
            for index in range(1, output_bands+1):
                scales_minmax += ((0, 255), )
        if input_dtype == "uint8":
            scale_method = None
            scales_minmax = ()
            for index in range(1, output_bands+1):
                scales_minmax += ((None, None), )

    # Create configuration
    config = dict(
        process="mapchete.processes.pyramid.tilify",
        output={
            "path": output_dir,
            "format": output_format,
            "bands": output_bands,
            "dtype": output_dtype
            },
        pyramid=dict(pixelbuffer=5, grid=pyramid_type),
        scale_method=scale_method,
        scales_minmax=scales_minmax,
        input={"raster": input_file},
        config_dir=os.getcwd(),
        zoom_levels=dict(min=minzoom, max=maxzoom),
        nodataval=nodataval,
        resampling=resampling,
        bounds=bounds,
        baselevel={"zoom": maxzoom, "resampling": resampling},
        mode=mode
    )

    # create process
    with mapchete.open(config, zoom=zoom, bounds=bounds) as mp:
        # prepare output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # run process
        mp.batch_process(zoom=[minzoom, maxzoom])