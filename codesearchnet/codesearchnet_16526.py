def _read_header(self, pltfile):
        """Read header bytes, try all possibilities for byte order/size/alignment."""
        nheader = struct.calcsize(self._headerfmt)
        names = [r.key for r in self._header_struct]
        binheader = pltfile.read(nheader)
        def decode_header(bsaflag='@'):
            h = dict(zip(names, struct.unpack(bsaflag+self._headerfmt, binheader)))
            h['bsaflag'] = bsaflag
            return h
        for flag in '@=<>':
            # try all endinaness and alignment options until we find something that looks sensible
            header = decode_header(flag)
            if header['rank'] == 3:
                break   # only legal value according to spec
            header = None
        if header is None:
            raise TypeError("Cannot decode header --- corrupted or wrong format?")
        for rec in self._header_struct:
            if not rec.is_legal_dict(header):
                warnings.warn("Key %s: Illegal value %r" % (rec.key, header[rec.key]))
        return header