def _debug_off():
    """ turns off debugging by removing hidden tmp file """
    if _os.path.exists(__debugflag__):
        _os.remove(__debugflag__)
    __loglevel__ = "ERROR"
    _LOGGER.info("debugging turned off")
    _set_debug_dict(__loglevel__)