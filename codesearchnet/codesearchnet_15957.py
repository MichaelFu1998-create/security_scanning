def strip_ampdu(self, idx):
        """strip(8 byte) radiotap.ampdu
        :idx: int
        :return: int
            idx
        :return: collections.namedtuple
        """
        ampdu = collections.namedtuple(
            'ampdu', ['reference', 'crc_val', 'reservered', 'flags'])
        flags = collections.namedtuple(
            'flags', ['report_zerolen', 'is_zerolen', 'lastknown', 'last',
                      'delim_crc_error'])

        idx = Radiotap.align(idx, 4)
        refnum, flag_vals, crc_val, reserved = struct.unpack_from('<LHBB', self._rtap, idx)
        ampdu.flags = flags
        ampdu.reference = refnum
        ampdu.crc_val = crc_val
        ampdu.reserved = reserved

        bits = format(flag_vals, '032b')[::-1]
        ampdu.flags.report_zerolen = int(bits[0])
        ampdu.flags.is_zerolen = int(bits[1])
        ampdu.flags.lastknown = int(bits[2])
        ampdu.flags.last = int(bits[3])
        ampdu.flags.delim_crc_error = int(bits[4])
        return idx + 8, ampdu