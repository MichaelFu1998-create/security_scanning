def read(adr, index_group, index_offset, plc_datatype, return_ctypes=False):
    # type: (AmsAddr, int, int, Type, bool) -> Any
    """Read data synchronous from an ADS-device.

        :param AmsAddr adr: local or remote AmsAddr
    :param int index_group: PLC storage area, according to the INDEXGROUP
        constants
    :param int index_offset: PLC storage address
    :param int plc_datatype: type of the data given to the PLC, according to
        PLCTYPE constants
    :param bool return_ctypes: return ctypes instead of python types if True
        (default: False)
    :return: value: **value**

    """
    if port is not None:
        return adsSyncReadReqEx2(
            port, adr, index_group, index_offset, plc_datatype, return_ctypes
        )

    return None