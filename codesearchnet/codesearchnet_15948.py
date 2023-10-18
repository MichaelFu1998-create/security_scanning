def strip_antenna(self, idx):
        """strip(1 byte) radiotap.antenna
        :return: int
            idx
        :return: int
        """
        antenna, = struct.unpack_from('<B', self._rtap, idx)
        return idx + 1, antenna