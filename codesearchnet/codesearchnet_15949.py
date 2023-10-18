def strip_db_antsignal(self, idx):
        """strip(1 byte) radiotap.db_antsignal
        :return: int
            idx
        :return: int
        """
        db_antsignal, = struct.unpack_from('<B', self._rtap, idx)
        return idx + 1, db_antsignal