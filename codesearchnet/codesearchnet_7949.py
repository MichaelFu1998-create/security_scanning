def write(adr, index_group, index_offset, value, plc_datatype):
    # type: (AmsAddr, int, int, Any, Type) -> None
    """Send data synchronous to an ADS-device.

    :param AmsAddr adr: local or remote AmsAddr
    :param int index_group: PLC storage area, according to the INDEXGROUP
        constants
    :param int index_offset: PLC storage address
    :param value: value to write to the storage address of the PLC
    :param Type plc_datatype: type of the data given to the PLC,
        according to PLCTYPE constants

    """
    if port is not None:
        return adsSyncWriteReqEx(
            port, adr, index_group, index_offset, value, plc_datatype
        )