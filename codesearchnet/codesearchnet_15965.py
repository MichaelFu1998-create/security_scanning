def strip_ccmp(self, idx):
        """strip(8 byte) wlan.ccmp.extiv
        CCMP Extended Initialization Vector
        :return: int
            number of processed bytes
        :return: ctypes.raw
            ccmp vector
        """
        ccmp_extiv = None
        if len(self._packet[idx:]) >= 8:
            raw_bytes = self._packet[idx:idx + 8]
            ccmp_extiv, = struct.unpack_from('Q', raw_bytes, 0)
        return 8, ccmp_extiv