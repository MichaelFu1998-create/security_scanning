def read(self, index_group, index_offset, plc_datatype, return_ctypes=False):
        # type: (int, int, Type, bool) -> Any
        """Read data synchronous from an ADS-device.

        :param int index_group: PLC storage area, according to the INDEXGROUP
            constants
        :param int index_offset: PLC storage address
        :param int plc_datatype: type of the data given to the PLC, according
            to PLCTYPE constants
            :return: value: **value**
        :param bool return_ctypes: return ctypes instead of python types if True
            (default: False)

        """
        if self._port is not None:
            return adsSyncReadReqEx2(
                self._port, self._adr, index_group, index_offset, plc_datatype, return_ctypes
            )

        return None