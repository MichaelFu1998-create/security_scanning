def WIFI(frame, no_rtap=False):
    """calls wifi packet discriminator and constructor.
    :frame: ctypes.Structure
    :no_rtap: Bool
    :return: packet object in success
    :return: int
        -1 on known error
    :return: int
        -2 on unknown error
    """
    pack = None
    try:
        pack = WiHelper.get_wifi_packet(frame, no_rtap)
    except Exception as e:
        logging.exception(e)
    return pack