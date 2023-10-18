def strip_flags(self, idx):
        """strip(1 byte) radiotap.flags
        :idx: int
        :return: int
            idx
        :return: collections.namedtuple
        """
        flags = collections.namedtuple(
            'flags', ['cfp', 'preamble', 'wep', 'fragmentation', 'fcs',
                      'datapad', 'badfcs', 'shortgi'])
        val, = struct.unpack_from('<B', self._rtap, idx)
        bits = format(val, '08b')[::-1]
        flags.cfp = int(bits[0])
        flags.preamble = int(bits[1])
        flags.wep = int(bits[2])
        flags.fragmentation = int(bits[3])
        flags.fcs = int(bits[4])
        flags.datapad = int(bits[5])
        flags.badfcs = int(bits[6])
        flags.shortgi = int(bits[7])
        return idx + 1, flags