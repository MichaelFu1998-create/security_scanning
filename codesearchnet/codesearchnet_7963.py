def write_by_name(self, data_name, value, plc_datatype):
        # type: (str, Any, Type) -> None
        """Send data synchronous to an ADS-device from data name.

        :param string data_name: PLC storage address
        :param value: value to write to the storage address of the PLC
        :param int plc_datatype: type of the data given to the PLC,
            according to PLCTYPE constants

        """
        if self._port:
            return adsSyncWriteByNameEx(
                self._port, self._adr, data_name, value, plc_datatype
            )