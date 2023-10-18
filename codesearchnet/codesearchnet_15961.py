def get_mac_addr(mac_addr):
        """converts bytes to mac addr format
        :mac_addr: ctypes.structure
        :return: str
            mac addr in format
            11:22:33:aa:bb:cc
        """
        mac_addr = bytearray(mac_addr)
        mac = b':'.join([('%02x' % o).encode('ascii') for o in mac_addr])
        return mac