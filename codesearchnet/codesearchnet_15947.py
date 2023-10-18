def strip_dbm_tx_power(self, idx):
        """strip(1 byte) dbm_tx_power
        :return: int
            idx
        :return: int
        """
        idx = Radiotap.align(idx, 1)
        dbm_tx_power, = struct.unpack_from('<b', self._rtap, idx)
        return idx + 1, dbm_tx_power