def adsSyncReadByNameEx(port, address, data_name, data_type, return_ctypes=False):
    # type: (int, AmsAddr, str, Type, bool) -> Any
    """Read data synchronous from an ADS-device from data name.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr address: local or remote AmsAddr
    :param string data_name: data name
    :param Type data_type: type of the data given to the PLC, according to
        PLCTYPE constants
    :param bool return_ctypes: return ctypes instead of python types if True
        (default: False)
    :rtype: data_type
    :return: value: **value**

    """
    # Get the handle of the PLC-variable
    handle = adsSyncReadWriteReqEx2(
        port,
        address,
        ADSIGRP_SYM_HNDBYNAME,
        0x0,
        PLCTYPE_UDINT,
        data_name,
        PLCTYPE_STRING,
    )

    # Read the value of a PLC-variable, via handle
    value = adsSyncReadReqEx2(
        port, address, ADSIGRP_SYM_VALBYHND, handle, data_type, return_ctypes
    )

    # Release the handle of the PLC-variable
    adsSyncWriteReqEx(port, address, ADSIGRP_SYM_RELEASEHND, 0, handle, PLCTYPE_UDINT)

    return value