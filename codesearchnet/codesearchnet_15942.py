def strip_dbm_antsignal(self, idx):
        """strip(1 byte) radiotap.dbm.ant_signal
        :idx: int
        :return: int
            idx
        :return: int
        """
        dbm_antsignal, = struct.unpack_from('<b', self._rtap, idx)
        return idx + 1, dbm_antsignal