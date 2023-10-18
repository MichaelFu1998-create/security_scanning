def strip_cntrl(payload):
        """strip(2 byte) wlan.ba.control
        :payload: ctypes.structure
        :return: int
            multitid (tid: traffic indicator)
        :return: int
            ackpolicy
        """
        cntrl = struct.unpack('H', payload)[0]
        cntrl_bits = format(cntrl, '016b')[::-1]
        ackpolicy = int(cntrl_bits[0])
        multitid = int(cntrl_bits[1])
        return ackpolicy, multitid