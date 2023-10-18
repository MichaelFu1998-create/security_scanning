def adsGetLocalAddressEx(port):
    # type: (int) -> AmsAddr
    """Return the local AMS-address and the port number.

    :rtype: pyads.structs.AmsAddr
    :return: AMS-address

    """
    get_local_address_ex = _adsDLL.AdsGetLocalAddressEx
    ams_address_struct = SAmsAddr()
    error_code = get_local_address_ex(port, ctypes.pointer(ams_address_struct))

    if error_code:
        raise ADSError(error_code)

    local_ams_address = AmsAddr()
    local_ams_address._ams_addr = ams_address_struct

    return local_ams_address