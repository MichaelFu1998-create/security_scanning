def read_by_name(self, data_name, plc_datatype, return_ctypes=False):
        # type: (str, Type, bool) -> Any
        """Read data synchronous from an ADS-device from data name.

        :param string data_name: data name
        :param int plc_datatype: type of the data given to the PLC, according
            to PLCTYPE constants
            :return: value: **value**
        :param bool return_ctypes: return ctypes instead of python types if True
            (default: False)

        """
        if self._port:
            return adsSyncReadByNameEx(self._port, self._adr, data_name, plc_datatype, return_ctypes)

        return None