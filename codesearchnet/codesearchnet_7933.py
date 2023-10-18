def adsPortCloseEx(port):
    # type: (int) -> None
    """Close the connection to the TwinCAT message router."""
    port_close_ex = _adsDLL.AdsPortCloseEx
    port_close_ex.restype = ctypes.c_long
    error_code = port_close_ex(port)

    if error_code:
        raise ADSError(error_code)