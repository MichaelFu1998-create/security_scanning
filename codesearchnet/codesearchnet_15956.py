def strip_mcs(self, idx):
        """strip(3 byte) radiotap.mcs which contains 802.11n bandwidth,
        mcs(modulation and coding scheme) and stbc(space time block coding)
        information.
        :idx: int
        :return: int
            idx
        :return: collections.namedtuple
        """
        mcs = collections.namedtuple(
            'mcs', ['known', 'index', 'have_bw', 'have_mcs', 'have_gi',
                    'have_format', 'have_fec', 'have_stbc', 'have_ness',
                    'ness_bit1'])

        idx = Radiotap.align(idx, 1)
        known, flags, index = struct.unpack_from('<BBB', self._rtap, idx)
        bits = format(flags, '032b')[::-1]

        mcs.known = known               # Known MCS information
        mcs.index = index               # MCS index
        mcs.have_bw = int(bits[0])      # Bandwidth
        mcs.have_mcs = int(bits[1])     # MCS
        mcs.have_gi = int(bits[2])      # Guard Interval
        mcs.have_format = int(bits[3])  # Format
        mcs.have_fec = int(bits[4])     # FEC(Forward Error Correction) type
        mcs.have_stbc = int(bits[5])    # Space Time Block Coding
        mcs.have_ness = int(bits[6])    # Number of Extension Spatial Streams
        mcs.ness_bit1 = int(bits[7])    # Number of Extension Spatial Streams bit 1
        return idx + 3, mcs