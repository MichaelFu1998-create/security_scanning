def open(
    config, mode="continue", zoom=None, bounds=None, single_input_file=None,
    with_cache=False, debug=False
):
    """
    Open a Mapchete process.

    Parameters
    ----------
    config : MapcheteConfig object, config dict or path to mapchete file
        Mapchete process configuration
    mode : string
        * ``memory``: Generate process output on demand without reading
          pre-existing data or writing new data.
        * ``readonly``: Just read data without processing new data.
        * ``continue``: (default) Don't overwrite existing output.
        * ``overwrite``: Overwrite existing output.
    zoom : list or integer
        process zoom level or a pair of minimum and maximum zoom level
    bounds : tuple
        left, bottom, right, top process boundaries in output pyramid
    single_input_file : string
        single input file if supported by process
    with_cache : bool
        process output data cached in memory

    Returns
    -------
    Mapchete
        a Mapchete process object
    """
    return Mapchete(
        MapcheteConfig(
            config, mode=mode, zoom=zoom, bounds=bounds,
            single_input_file=single_input_file, debug=debug),
        with_cache=with_cache)