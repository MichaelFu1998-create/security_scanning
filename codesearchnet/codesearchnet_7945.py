def adsSyncSetTimeoutEx(port, nMs):
    # type: (int, int) -> None
    """Set Timeout.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param int nMs: timeout in ms

    """
    adsSyncSetTimeoutFct = _adsDLL.AdsSyncSetTimeoutEx
    cms = ctypes.c_long(nMs)
    err_code = adsSyncSetTimeoutFct(port, cms)
    if err_code:
        raise ADSError(err_code)