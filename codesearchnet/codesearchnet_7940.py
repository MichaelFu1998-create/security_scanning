def adsSyncReadReqEx2(
    port, address, index_group, index_offset, data_type, return_ctypes=False
):
    # type: (int, AmsAddr, int, int, Type, bool) -> Any
    """Read data synchronous from an ADS-device.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr address: local or remote AmsAddr
    :param int index_group: PLC storage area, according to the INDEXGROUP
        constants
    :param int index_offset: PLC storage address
    :param Type data_type: type of the data given to the PLC, according to
        PLCTYPE constants
    :param bool return_ctypes: return ctypes instead of python types if True
        (default: False)
    :rtype: data_type
    :return: value: **value**

    """
    sync_read_request = _adsDLL.AdsSyncReadReqEx2

    ams_address_pointer = ctypes.pointer(address.amsAddrStruct())
    index_group_c = ctypes.c_ulong(index_group)
    index_offset_c = ctypes.c_ulong(index_offset)

    if data_type == PLCTYPE_STRING:
        data = (STRING_BUFFER * PLCTYPE_STRING)()
    else:
        data = data_type()

    data_pointer = ctypes.pointer(data)
    data_length = ctypes.c_ulong(ctypes.sizeof(data))

    bytes_read = ctypes.c_ulong()
    bytes_read_pointer = ctypes.pointer(bytes_read)

    error_code = sync_read_request(
        port,
        ams_address_pointer,
        index_group_c,
        index_offset_c,
        data_length,
        data_pointer,
        bytes_read_pointer,
    )

    if error_code:
        raise ADSError(error_code)

    # If we're reading a value of predetermined size (anything but a string),
    # validate that the correct number of bytes were read
    if data_type != PLCTYPE_STRING and bytes_read.value != data_length.value:
        raise RuntimeError(
            "Insufficient data (expected {0} bytes, {1} were read).".format(
                data_length.value, bytes_read.value
            )
        )

    if return_ctypes:
        return data

    if data_type == PLCTYPE_STRING:
        return data.value.decode("utf-8")

    if type(data_type).__name__ == "PyCArrayType":
        return [i for i in data]

    if hasattr(data, "value"):
        return data.value

    return data