def available_input_formats():
    """
    Return all available input formats.

    Returns
    -------
    formats : list
        all available input formats
    """
    input_formats = []
    for v in pkg_resources.iter_entry_points(DRIVERS_ENTRY_POINT):
        logger.debug("driver found: %s", v)
        driver_ = v.load()
        if hasattr(driver_, "METADATA") and (driver_.METADATA["mode"] in ["r", "rw"]):
            input_formats.append(driver_.METADATA["driver_name"])
    return input_formats