def strip_rts_retries(self, idx):
        """strip(1 byte) rts_retries
        :idx: int
        :return: int
            idx
        :return: int
        """
        rts_retries, = struct.unpack_from('<B', self._rtap, idx)
        return idx + 1, rts_retries