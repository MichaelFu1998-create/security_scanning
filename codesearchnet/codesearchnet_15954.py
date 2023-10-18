def strip_data_retries(self, idx):
        """strip(1 byte) data_retries
        :idx: int
        :return: int
            idx
        :return: int
        """
        data_retries, = struct.unpack_from('<B', self._rtap, idx)
        return idx + 1, data_retries