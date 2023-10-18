def strip_dbm_antnoise(self, idx):
        """strip(1 byte) radiotap.dbm_antnoise
        :idx: int
        :return: int
            idx
        :return: int
        """
        dbm_antnoise, = struct.unpack_from('<b', self._rtap, idx)
        return idx + 1, dbm_antnoise