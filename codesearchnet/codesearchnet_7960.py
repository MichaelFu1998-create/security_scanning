def read_write(
        self,
        index_group,
        index_offset,
        plc_read_datatype,
        value,
        plc_write_datatype,
        return_ctypes=False,
    ):
        # type: (int, int, Type, Any, Type, bool) -> Any
        """Read and write data synchronous from/to an ADS-device.

        :param int index_group: PLC storage area, according to the INDEXGROUP
            constants
        :param int index_offset: PLC storage address
        :param int plc_read_datatype: type of the data given to the PLC to
            respond to, according to PLCTYPE constants
        :param value: value to write to the storage address of the PLC
        :param plc_write_datatype: type of the data given to the PLC,
            according to PLCTYPE constants
            :rtype: PLCTYPE
    :param bool return_ctypes: return ctypes instead of python types if True
        (default: False)
        :return: value: **value**

        """
        if self._port is not None:
            return adsSyncReadWriteReqEx2(
                self._port,
                self._adr,
                index_group,
                index_offset,
                plc_read_datatype,
                value,
                plc_write_datatype,
                return_ctypes,
            )

        return None