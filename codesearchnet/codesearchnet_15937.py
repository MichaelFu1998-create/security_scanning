def strip_tsft(self, idx):
        """strip(8 byte) radiotap.mactime
        :idx: int
        :return: int
            idx
        :return: int
            mactime
        """
        idx = Radiotap.align(idx, 8)
        mactime, = struct.unpack_from('<Q', self._rtap, idx)
        return idx + 8, mactime