def strip_xchannel(self, idx):
        """strip(7 bytes) radiotap.xchannel.channel(1 byte),
        radiotap.xchannel.freq(2 bytes) and radiotap.xchannel.flags(4 bytes)
        :idx: int
        :return: int
            idx
        :return: collections.namedtuple
        """
        xchannel = collections.namedtuple(
            'xchannel', ['flags', 'freq', 'channel', 'max_power'])

        flags = collections.namedtuple(
            'flags', ['turbo', 'cck', 'ofdm', 'two_g', 'five_g', 'passive',
                      'dynamic', 'gfsk', 'gsm', 'sturbo', 'hafl', 'quarter',
                      'ht_20', 'ht_40u', 'ht_40d'])

        idx = Radiotap.align(idx, 2)
        flag_val, freq, channel, max_power = struct.unpack_from('<lHBB', self._rtap, idx)

        xchannel.freq = freq
        xchannel.channel = channel
        xchannel.max_power = max_power

        bits = format(flag_val, '032b')[::-1]
        flags.turbo = int(bits[4])
        flags.cck = int(bits[5])
        flags.ofdm = int(bits[6])
        flags.two_g = int(bits[7])
        flags.five_g = int(bits[8])
        flags.passive = int(bits[9])
        flags.dynamic = int(bits[10])
        flags.gfsk = int(bits[11])
        flags.gsm = int(bits[12])
        flags.sturbo = int(bits[13])
        flags.half = int(bits[14])
        flags.quarter = int(bits[15])
        flags.ht_20 = int(bits[16])
        flags.ht_40u = int(bits[17])
        flags.ht_40d = int(bits[18])
        xchannel.flags = flags

        return idx + 8, xchannel