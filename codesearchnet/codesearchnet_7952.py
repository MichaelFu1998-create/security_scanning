def read_by_name(adr, data_name, plc_datatype, return_ctypes=False):
    # type: (AmsAddr, str, Type, bool) -> Any
    """Read data synchronous from an ADS-device from data name.

    :param AmsAddr adr: local or remote AmsAddr
    :param string data_name: data name
    :param int plc_datatype: type of the data given to the PLC, according to
        PLCTYPE constants
    :param bool return_ctypes: return ctypes instead of python types if True
        (default: False)
    :return: value: **value**

    """
    if port is not None:
        return adsSyncReadByNameEx(port, adr, data_name, plc_datatype, return_ctypes)

    return None