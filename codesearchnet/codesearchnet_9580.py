def load_input_reader(input_params, readonly=False):
    """
    Return input class of driver.

    Returns
    -------
    input_params : ``InputData``
        input parameters
    """
    logger.debug("find input reader with params %s", input_params)
    if not isinstance(input_params, dict):
        raise TypeError("input_params must be a dictionary")
    if "abstract" in input_params:
        driver_name = input_params["abstract"]["format"]
    elif "path" in input_params:
        if os.path.splitext(input_params["path"])[1]:
            input_file = input_params["path"]
            driver_name = driver_from_file(input_file)
        else:
            logger.debug("%s is a directory", input_params["path"])
            driver_name = "TileDirectory"
    else:
        raise MapcheteDriverError("invalid input parameters %s" % input_params)
    for v in pkg_resources.iter_entry_points(DRIVERS_ENTRY_POINT):
        driver_ = v.load()
        if hasattr(driver_, "METADATA") and (
            driver_.METADATA["driver_name"] == driver_name
        ):
            return v.load().InputData(input_params, readonly=readonly)
    raise MapcheteDriverError("no loader for driver '%s' could be found." % driver_name)