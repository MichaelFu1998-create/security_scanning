def strip_vht(self, idx):
        """strip(12 byte) radiotap.vht
        :idx: int
        :return: int
            idx
        :return: collections.namedtuple
        """
        vht = collections.namedtuple(
            'vht', ['known_bits', 'have_stbc', 'have_txop_ps', 'have_gi',
                    'have_sgi_nsym_da', 'have_ldpc_extra', 'have_beamformed',
                    'have_bw', 'have_gid', 'have_paid', 'stbc', 'txop_ps', 'gi',
                    'sgi_nysm_da', 'ldpc_extra', 'group_id', 'partial_id',
                    'beamformed', 'user_0', 'user_1', 'user_2', 'user_3'])
        user = collections.namedtuple('user', ['nss', 'mcs', 'coding'])

        idx = Radiotap.align(idx, 2)
        known, flags, bw = struct.unpack_from('<HBB', self._rtap, idx)
        mcs_nss_0, mcs_nss_1, mcs_nss_2, mcs_nss_3 = struct.unpack_from('<BBBB', self._rtap, idx + 4)
        coding, group_id, partial_id = struct.unpack_from('<BBH', self._rtap, idx + 8)

        known_bits = format(known, '032b')[::-1]
        vht.known_bits = known_bits
        vht.have_stbc = int(known_bits[0])         # Space Time Block Coding
        vht.have_txop_ps = int(known_bits[1])      # TXOP_PS_NOT_ALLOWD
        vht.have_gi = int(known_bits[2])           # Short/Long Guard Interval
        vht.have_sgi_nsym_da = int(known_bits[3])  # Short Guard Interval Nsym Disambiguation
        vht.have_ldpc_extra = int(known_bits[4])   # LDPC(Low Density Parity Check)
        vht.have_beamformed = int(known_bits[5])   # Beamformed
        vht.have_bw = int(known_bits[6])           # Bandwidth
        vht.have_gid = int(known_bits[7])          # Group ID
        vht.have_paid = int(known_bits[8])         # Partial AID

        flag_bits = format(flags, '032b')[::-1]
        vht.flag_bits = flag_bits
        vht.stbc = int(flag_bits[0])
        vht.txop_ps = int(flag_bits[1])
        vht.gi = int(flag_bits[2])
        vht.sgi_nysm_da = int(flag_bits[3])
        vht.ldpc_extra = int(flag_bits[4])
        vht.beamformed = int(flag_bits[5])
        vht.group_id = group_id
        vht.partial_id = partial_id

        vht.bw = bw
        vht.user_0 = user(None, None, None)
        vht.user_1 = user(None, None, None)
        vht.user_2 = user(None, None, None)
        vht.user_3 = user(None, None, None)
        for (i, mcs_nss) in enumerate([mcs_nss_0, mcs_nss_1, mcs_nss_2, mcs_nss_3]):
            if mcs_nss:
                nss = mcs_nss & 0xf0 >> 4
                mcs = (mcs_nss & 0xf0) >> 4
                coding = (coding & 2**i) >> i
                if i == 0:
                    vht.user_0 = user(nss, mcs, coding)
                elif i == 1:
                    vht.user_1 = user(nss, mcs, coding)
                elif i == 2:
                    vht.user_2 = user(nss, mcs, coding)
                elif i == 3:
                    vht.user_3 = user(nss, mcs, coding)

        return idx + 12, vht