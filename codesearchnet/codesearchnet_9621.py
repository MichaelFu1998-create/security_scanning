def serve(
    mapchete_file,
    port=None,
    internal_cache=None,
    zoom=None,
    bounds=None,
    overwrite=False,
    readonly=False,
    memory=False,
    input_file=None,
    debug=False,
    logfile=None
):
    """
    Serve a Mapchete process.

    Creates the Mapchete host and serves both web page with OpenLayers and the
    WMTS simple REST endpoint.
    """
    app = create_app(
        mapchete_files=[mapchete_file], zoom=zoom,
        bounds=bounds, single_input_file=input_file,
        mode=_get_mode(memory, readonly, overwrite), debug=debug
    )
    if os.environ.get("MAPCHETE_TEST") == "TRUE":
        logger.debug("don't run flask app, MAPCHETE_TEST environment detected")
    else:
        app.run(
            threaded=True, debug=True, port=port, host='0.0.0.0',
            extra_files=[mapchete_file]
        )