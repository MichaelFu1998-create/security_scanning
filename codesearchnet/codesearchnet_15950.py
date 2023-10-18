def strip_db_antnoise(self, idx):
        """strip(1 byte) radiotap.db_antnoise
        :return: int
            idx
        :return: int
        """
        db_antnoise, = struct.unpack_from('<B', self._rtap, idx)
        return idx + 1, db_antnoise