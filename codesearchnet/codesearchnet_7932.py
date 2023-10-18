def adsPortOpenEx():
    # type: () -> int
    """Connect to the TwinCAT message router.

    :rtype: int
    :return: port number

    """
    port_open_ex = _adsDLL.AdsPortOpenEx
    port_open_ex.restype = ctypes.c_long
    port = port_open_ex()

    if port == 0:
        raise RuntimeError("Failed to open port on AMS router.")

    return port