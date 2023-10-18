def write_by_name(adr, data_name, value, plc_datatype):
    # type: (AmsAddr, str, Any, Type) -> None
    """Send data synchronous to an ADS-device from data name.

    :param AmsAddr adr: local or remote AmsAddr
    :param string data_name: PLC storage address
    :param value: value to write to the storage address of the PLC
    :param int plc_datatype: type of the data given to the PLC,
        according to PLCTYPE constants

    """
    if port is not None:
        return adsSyncWriteByNameEx(port, adr, data_name, value, plc_datatype)