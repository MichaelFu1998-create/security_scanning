def strip_lock_quality(self, idx):
        """strip(2 byte) lock quality
        :idx: int
        :return: int
            idx
        :return: int
        """
        idx = Radiotap.align(idx, 2)
        lock_quality, = struct.unpack_from('<H', self._rtap, idx)
        return idx + 2, lock_quality