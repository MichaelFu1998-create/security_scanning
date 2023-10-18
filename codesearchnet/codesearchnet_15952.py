def strip_tx_flags(self, idx):
        """strip(1 byte) tx_flags
        :idx: int
        :return: int
            idx
        :return: int
        """
        idx = Radiotap.align(idx, 2)
        tx_flags, = struct.unpack_from('<B', self._rtap, idx)
        return idx + 1, tx_flags