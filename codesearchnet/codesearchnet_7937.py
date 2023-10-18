def adsSyncWriteControlReqEx(
    port, address, ads_state, device_state, data, plc_data_type
):
    # type: (int, AmsAddr, int, int, Any, Type) -> None
    """Change the ADS state and the machine-state of the ADS-server.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr adr: local or remote AmsAddr
    :param int ads_state: new ADS-state, according to ADSTATE constants
    :param int device_state: new machine-state
    :param data: additional data
    :param int plc_data_type: plc datatype, according to PLCTYPE constants

    """
    sync_write_control_request = _adsDLL.AdsSyncWriteControlReqEx

    ams_address_pointer = ctypes.pointer(address.amsAddrStruct())
    ads_state_c = ctypes.c_ulong(ads_state)
    device_state_c = ctypes.c_ulong(device_state)

    if plc_data_type == PLCTYPE_STRING:
        data = ctypes.c_char_p(data.encode("utf-8"))
        data_pointer = data
        data_length = len(data_pointer.value) + 1
    else:
        data = plc_data_type(data)
        data_pointer = ctypes.pointer(data)
        data_length = ctypes.sizeof(data)

    error_code = sync_write_control_request(
        port,
        ams_address_pointer,
        ads_state_c,
        device_state_c,
        data_length,
        data_pointer,
    )

    if error_code:
        raise ADSError(error_code)