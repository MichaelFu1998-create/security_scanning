def load_output_writer(output_params, readonly=False):
    """
    Return output class of driver.

    Returns
    -------
    output : ``OutputData``
        output writer object
    """
    if not isinstance(output_params, dict):
        raise TypeError("output_params must be a dictionary")
    driver_name = output_params["format"]
    for v in pkg_resources.iter_entry_points(DRIVERS_ENTRY_POINT):
        _driver = v.load()
        if all(
            [hasattr(_driver, attr) for attr in ["OutputData", "METADATA"]]
            ) and (
            _driver.METADATA["driver_name"] == driver_name
        ):
            return _driver.OutputData(output_params, readonly=readonly)
    raise MapcheteDriverError("no loader for driver '%s' could be found." % driver_name)