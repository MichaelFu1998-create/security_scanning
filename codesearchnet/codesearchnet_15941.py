def strip_fhss(self, idx):
        """strip (2 byte) radiotap.fhss.hopset(1 byte) and
        radiotap.fhss.pattern(1 byte)
        :idx: int
        :return: int
            idx
        :return: collections.namedtuple
        """
        fhss = collections.namedtuple('fhss', ['hopset', 'pattern'])
        fhss.hopset, fhss.pattern, = struct.unpack_from('<bb', self._rtap, idx)
        return idx + 2, fhss