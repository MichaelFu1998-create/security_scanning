def strip_db_tx_attenuation(self, idx):
        """strip(1 byte) db_tx_attenuation
        :return: int
            idx
        :return: int
        """
        idx = Radiotap.align(idx, 2)
        db_tx_attenuation, = struct.unpack_from('<H', self._rtap, idx)
        return idx + 2, db_tx_attenuation