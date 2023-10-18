def strip_rx_flags(self, idx):
        """strip(2 byte) radiotap.rxflags
        :idx: int
        :return: int
            idx
        :return: collections.namedtuple
        """
        rx_flags = collections.namedtuple('rx_flags', ['reserved', 'badplcp'])

        idx = Radiotap.align(idx, 2)
        flags, = struct.unpack_from('<H', self._rtap, idx)
        flag_bits = format(flags, '08b')[::-1]
        rx_flags.reserved = int(flag_bits[0])
        rx_flags.badplcp = int(flag_bits[1])
        return idx + 2, rx_flags