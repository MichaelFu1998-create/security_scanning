def strip_ssc(payload):
        """strip(2 byte) wlan_mgt.fixed.ssc
        :payload: ctypes.structure
        :return: int
            ssc_seq (starting sequence control sequence)
        :return: int
            ssc_frag (starting sequence control fragment number)
        """
        ssc = struct.unpack('H', payload)[0]
        ssc_seq = ssc >> 4
        ssc_frag = ssc & 0x000f
        return ssc_seq, ssc_frag