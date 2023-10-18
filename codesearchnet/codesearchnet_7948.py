def write_control(adr, ads_state, device_state, data, plc_datatype):
    # type: (AmsAddr, int, int, Any, Type) -> None
    """Change the ADS state and the machine-state of the ADS-server.

    :param AmsAddr adr: local or remote AmsAddr
    :param int ads_state: new ADS-state, according to ADSTATE constants
    :param int device_state: new machine-state
    :param data: additional data
    :param int plc_datatype: datatype, according to PLCTYPE constants

    :note: Despite changing the ADS-state and the machine-state it is possible
           to send additional data to the ADS-server. For current ADS-devices
           additional data is not progressed.
           Every ADS-device is able to communicate its current state to other
           devices.
           There is a difference between the device-state and the state of the
           ADS-interface (AdsState). The possible states of an ADS-interface
           are defined in the ADS-specification.

    """
    if port is not None:
        return adsSyncWriteControlReqEx(
            port, adr, ads_state, device_state, data, plc_datatype
        )