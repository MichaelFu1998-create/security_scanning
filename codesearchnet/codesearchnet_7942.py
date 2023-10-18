def adsSyncWriteByNameEx(port, address, data_name, value, data_type):
    # type: (int, AmsAddr, str, Any, Type) -> None
    """Send data synchronous to an ADS-device from data name.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr address: local or remote AmsAddr
    :param string data_name: PLC storage address
    :param value: value to write to the storage address of the PLC
    :param Type data_type: type of the data given to the PLC,
        according to PLCTYPE constants

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

    # Write the value of a PLC-variable, via handle
    adsSyncWriteReqEx(port, address, ADSIGRP_SYM_VALBYHND, handle, value, data_type)

    # Release the handle of the PLC-variable
    adsSyncWriteReqEx(port, address, ADSIGRP_SYM_RELEASEHND, 0, handle, PLCTYPE_UDINT)