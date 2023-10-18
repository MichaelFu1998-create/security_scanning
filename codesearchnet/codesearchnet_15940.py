def strip_chan(self, idx):
        """strip(2 byte) radiotap.channel.flags
        :idx: int
        :return: int
            idx
        :return: collections.namedtuple
        """
        chan = collections.namedtuple(
            'chan', ['freq', 'turbo', 'cck', 'ofdm', 'two_g', 'five_g',
                     'passive', 'dynamic', 'gfsk', 'gsm', 'static_turbo',
                     'half_rate', 'quarter_rate'])

        idx = Radiotap.align(idx, 2)
        freq, flags, = struct.unpack_from('<HH', self._rtap, idx)
        chan.freq = freq

        bits = format(flags, '016b')[::-1]
        chan.turbo = int(bits[4])
        chan.cck = int(bits[5])
        chan.ofdm = int(bits[6])
        chan.two_g = int(bits[7])
        chan.five_g = int(bits[8])
        chan.passive = int(bits[9])
        chan.dynamic = int(bits[10])
        chan.gfsk = int(bits[11])
        chan.gsm = int(bits[12])
        chan.static_turbo = int(bits[13])
        chan.half_rate = int(bits[14])
        chan.quarter_rate = int(bits[15])
        return idx + 4, chan