def adsSyncWriteReqEx(port, address, index_group, index_offset, value, plc_data_type):
    # type: (int, AmsAddr, int, int, Any, Type) -> None
    """Send data synchronous to an ADS-device.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr address: local or remote AmsAddr
    :param int indexGroup: PLC storage area, according to the INDEXGROUP
        constants
    :param int index_offset: PLC storage address
    :param value: value to write to the storage address of the PLC
    :param int plc_data_type: type of the data given to the PLC,
        according to PLCTYPE constants

    """
    sync_write_request = _adsDLL.AdsSyncWriteReqEx

    ams_address_pointer = ctypes.pointer(address.amsAddrStruct())
    index_group_c = ctypes.c_ulong(index_group)
    index_offset_c = ctypes.c_ulong(index_offset)

    if plc_data_type == PLCTYPE_STRING:
        data = ctypes.c_char_p(value.encode("utf-8"))
        data_pointer = data  # type: Union[ctypes.c_char_p, ctypes.pointer]
        data_length = len(data_pointer.value) + 1  # type: ignore

    else:
        if type(plc_data_type).__name__ == "PyCArrayType":
            data = plc_data_type(*value)
        else:
            data = plc_data_type(value)

        data_pointer = ctypes.pointer(data)
        data_length = ctypes.sizeof(data)

    error_code = sync_write_request(
        port,
        ams_address_pointer,
        index_group_c,
        index_offset_c,
        data_length,
        data_pointer,
    )

    if error_code:
        raise ADSError(error_code)