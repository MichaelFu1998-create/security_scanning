def strip_tx_attenuation(self, idx):
        """strip(1 byte) tx_attenuation
        :idx: int
        :return: int
            idx
        :return: int
        """
        idx = Radiotap.align(idx, 2)
        tx_attenuation, = struct.unpack_from('<H', self._rtap, idx)
        return idx + 2, tx_attenuation