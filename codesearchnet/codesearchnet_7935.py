def adsSyncReadStateReqEx(port, address):
    # type: (int, AmsAddr) -> Tuple[int, int]
    """Read the current ADS-state and the machine-state.

    Read the current ADS-state and the machine-state from the
    ADS-server.

    :param pyads.structs.AmsAddr address: local or remote AmsAddr
    :rtype: (int, int)
    :return: ads_state, device_state

    """
    sync_read_state_request = _adsDLL.AdsSyncReadStateReqEx

    # C pointer to ams address struct
    ams_address_pointer = ctypes.pointer(address.amsAddrStruct())

    # Current ADS status and corresponding pointer
    ads_state = ctypes.c_int()
    ads_state_pointer = ctypes.pointer(ads_state)

    # Current device status and corresponding pointer
    device_state = ctypes.c_int()
    device_state_pointer = ctypes.pointer(device_state)

    error_code = sync_read_state_request(
        port, ams_address_pointer, ads_state_pointer, device_state_pointer
    )

    if error_code:
        raise ADSError(error_code)

    return (ads_state.value, device_state.value)