def adsSyncReadWriteReqEx2(
    port,
    address,
    index_group,
    index_offset,
    read_data_type,
    value,
    write_data_type,
    return_ctypes=False,
):
    # type: (int, AmsAddr, int, int, Type, Any, Type, bool) -> Any
    """Read and write data synchronous from/to an ADS-device.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr address: local or remote AmsAddr
    :param int index_group: PLC storage area, according to the INDEXGROUP
        constants
    :param int index_offset: PLC storage address
    :param Type read_data_type: type of the data given to the PLC to respond to,
        according to PLCTYPE constants
    :param value: value to write to the storage address of the PLC
    :param Type write_data_type: type of the data given to the PLC, according to
        PLCTYPE constants
    :param bool return_ctypes: return ctypes instead of python types if True
        (default: False)
    :rtype: read_data_type
    :return: value: value read from PLC

    """
    sync_read_write_request = _adsDLL.AdsSyncReadWriteReqEx2

    ams_address_pointer = ctypes.pointer(address.amsAddrStruct())
    index_group_c = ctypes.c_ulong(index_group)
    index_offset_c = ctypes.c_ulong(index_offset)

    if read_data_type == PLCTYPE_STRING:
        read_data = (STRING_BUFFER * PLCTYPE_STRING)()
    else:
        read_data = read_data_type()

    read_data_pointer = ctypes.pointer(read_data)
    read_length = ctypes.c_ulong(ctypes.sizeof(read_data))

    bytes_read = ctypes.c_ulong()
    bytes_read_pointer = ctypes.pointer(bytes_read)

    if write_data_type == PLCTYPE_STRING:
        # Get pointer to string
        write_data_pointer = ctypes.c_char_p(
            value.encode("utf-8")
        )  # type: Union[ctypes.c_char_p, ctypes.pointer]  # noqa: E501
        # Add an extra byte to the data length for the null terminator
        write_length = len(value) + 1
    else:
        if type(write_data_type).__name__ == "PyCArrayType":
            write_data = write_data_type(*value)
        else:
            write_data = write_data_type(value)
        write_data_pointer = ctypes.pointer(write_data)
        write_length = ctypes.sizeof(write_data)

    err_code = sync_read_write_request(
        port,
        ams_address_pointer,
        index_group_c,
        index_offset_c,
        read_length,
        read_data_pointer,
        write_length,
        write_data_pointer,
        bytes_read_pointer,
    )

    if err_code:
        raise ADSError(err_code)

    # If we're reading a value of predetermined size (anything but a string),
    # validate that the correct number of bytes were read
    if read_data_type != PLCTYPE_STRING and bytes_read.value != read_length.value:
        raise RuntimeError(
            "Insufficient data (expected {0} bytes, {1} were read).".format(
                read_length.value, bytes_read.value
            )
        )

    if return_ctypes:
        return read_data

    if read_data_type == PLCTYPE_STRING:
        return read_data.value.decode("utf-8")

    if type(read_data_type).__name__ == "PyCArrayType":
        return [i for i in read_data]

    if hasattr(read_data, "value"):
        return read_data.value

    return read_data