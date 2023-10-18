def available_output_formats():
    """
    Return all available output formats.

    Returns
    -------
    formats : list
        all available output formats
    """
    output_formats = []
    for v in pkg_resources.iter_entry_points(DRIVERS_ENTRY_POINT):
        driver_ = v.load()
        if hasattr(driver_, "METADATA") and (
            driver_.METADATA["mode"] in ["w", "rw"]
        ):
            output_formats.append(driver_.METADATA["driver_name"])
    return output_formats