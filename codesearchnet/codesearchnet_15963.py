def strip_seq_cntrl(self, idx):
        """strip(2 byte) wlan.seq(12 bit) and wlan.fram(4 bit)
        number information.
        :seq_cntrl: ctypes.Structure
        :return: int
            sequence number
        :return: int
            fragment number
        """
        seq_cntrl = struct.unpack('H', self._packet[idx:idx + 2])[0]
        seq_num = seq_cntrl >> 4
        frag_num = seq_cntrl & 0x000f
        return seq_num, frag_num