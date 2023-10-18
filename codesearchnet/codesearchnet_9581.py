def driver_from_file(input_file):
    """
    Guess driver from file extension.

    Returns
    -------
    driver : string
        driver name
    """
    file_ext = os.path.splitext(input_file)[1].split(".")[1]
    if file_ext not in _file_ext_to_driver():
        raise MapcheteDriverError(
            "no driver could be found for file extension %s" % file_ext
        )
    driver = _file_ext_to_driver()[file_ext]
    if len(driver) > 1:
        warnings.warn(
            DeprecationWarning(
                "more than one driver for file found, taking %s" % driver[0]
            )
        )
    return driver[0]