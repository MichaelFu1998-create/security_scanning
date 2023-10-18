def _debug_on():
    """
    Turns on debugging by creating hidden tmp file
    This is only run by the __main__ engine.
    """
    ## make tmp file and set loglevel for top-level init
    with open(__debugflag__, 'w') as dfile:
        dfile.write("wat")
    __loglevel__ = "DEBUG"
    _LOGGER.info("debugging turned on and registered to be turned off at exit")
    _set_debug_dict(__loglevel__)