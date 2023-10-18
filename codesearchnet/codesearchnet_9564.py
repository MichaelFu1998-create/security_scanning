def zoom_index_gen(
    mp=None,
    out_dir=None,
    zoom=None,
    geojson=False,
    gpkg=False,
    shapefile=False,
    txt=False,
    vrt=False,
    fieldname="location",
    basepath=None,
    for_gdal=True,
    threading=False,
):
    """
    Generate indexes for given zoom level.

    Parameters
    ----------
    mp : Mapchete object
        process output to be indexed
    out_dir : path
        optionally override process output directory
    zoom : int
        zoom level to be processed
    geojson : bool
        generate GeoJSON index (default: False)
    gpkg : bool
        generate GeoPackage index (default: False)
    shapefile : bool
        generate Shapefile index (default: False)
    txt : bool
        generate tile path list textfile (default: False)
    vrt : bool
        GDAL-style VRT file (default: False)
    fieldname : str
        field name which contains paths of tiles (default: "location")
    basepath : str
        if set, use custom base path instead of output path
    for_gdal : bool
        use GDAL compatible remote paths, i.e. add "/vsicurl/" before path
        (default: True)
    """
    for zoom in get_zoom_levels(process_zoom_levels=zoom):
        with ExitStack() as es:
            # get index writers for all enabled formats
            index_writers = []
            if geojson:
                index_writers.append(
                    es.enter_context(
                        VectorFileWriter(
                            driver="GeoJSON",
                            out_path=_index_file_path(out_dir, zoom, "geojson"),
                            crs=mp.config.output_pyramid.crs,
                            fieldname=fieldname
                        )
                    )
                )
            if gpkg:
                index_writers.append(
                    es.enter_context(
                        VectorFileWriter(
                            driver="GPKG",
                            out_path=_index_file_path(out_dir, zoom, "gpkg"),
                            crs=mp.config.output_pyramid.crs,
                            fieldname=fieldname
                        )
                    )
                )
            if shapefile:
                index_writers.append(
                    es.enter_context(
                        VectorFileWriter(
                            driver="ESRI Shapefile",
                            out_path=_index_file_path(out_dir, zoom, "shp"),
                            crs=mp.config.output_pyramid.crs,
                            fieldname=fieldname
                        )
                    )
                )
            if txt:
                index_writers.append(
                    es.enter_context(
                        TextFileWriter(out_path=_index_file_path(out_dir, zoom, "txt"))
                    )
                )
            if vrt:
                index_writers.append(
                    es.enter_context(
                        VRTFileWriter(
                            out_path=_index_file_path(out_dir, zoom, "vrt"),
                            output=mp.config.output,
                            out_pyramid=mp.config.output_pyramid
                        )
                    )
                )

            logger.debug("use the following index writers: %s", index_writers)

            def _worker(tile):
                # if there are indexes to write to, check if output exists
                tile_path = _tile_path(
                    orig_path=mp.config.output.get_path(tile),
                    basepath=basepath,
                    for_gdal=for_gdal
                )
                indexes = [
                    i for i in index_writers
                    if not i.entry_exists(tile=tile, path=tile_path)
                ]
                if indexes:
                    output_exists = mp.config.output.tiles_exist(output_tile=tile)
                else:
                    output_exists = None
                return tile, tile_path, indexes, output_exists

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for task in concurrent.futures.as_completed(
                    (
                        executor.submit(_worker, i)
                        for i in mp.config.output_pyramid.tiles_from_geom(
                            mp.config.area_at_zoom(zoom), zoom
                        )
                    )
                ):
                    tile, tile_path, indexes, output_exists = task.result()
                    # only write entries if there are indexes to write to and output
                    # exists
                    if indexes and output_exists:
                        logger.debug("%s exists", tile_path)
                        logger.debug("write to %s indexes" % len(indexes))
                        for index in indexes:
                            index.write(tile, tile_path)
                    # yield tile for progress information
                    yield tile