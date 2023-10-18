def _read_header(self, ccp4file):
        """Read header bytes"""

        bsaflag = self._detect_byteorder(ccp4file)

        # Parse the top of the header (4-byte words, 1 to 25).
        nheader = struct.calcsize(self._headerfmt)
        names = [r.key for r in self._header_struct]
        bintopheader = ccp4file.read(25 * 4)

        def decode_header(header, bsaflag='@'):
            h = dict(zip(names, struct.unpack(bsaflag + self._headerfmt,
                                              header)))
            h['bsaflag'] = bsaflag
            return h

        header = decode_header(bintopheader, bsaflag)
        for rec in self._header_struct:
            if not rec.is_legal_dict(header):
                warnings.warn(
                    "Key %s: Illegal value %r" % (rec.key, header[rec.key]))

        # Parse the latter half of the header (4-byte words, 26 to 256).
        if (header['lskflg']):
            skewmatrix = np.fromfile(ccp4file, dtype=np.float32, count=9)
            header['skwmat'] = skewmatrix.reshape((3, 3))
            header['skwtrn'] = np.fromfile(ccp4file, dtype=np.float32, count=3)
        else:
            header['skwmat'] = header['skwtrn'] = None
            ccp4file.seek(12 * 4, 1)
        ccp4file.seek(15 * 4, 1)  # Skip future use section.
        ccp4file.seek(4, 1)  # Skip map text, already used above to verify format.
        # TODO: Compare file specified endianness to one obtained above.
        endiancode = struct.unpack(bsaflag + '4b', ccp4file.read(4))
        header['endianness'] = 'little' if endiancode == (0x44, 0x41, 0, 0
                                                          ) else 'big'
        header['arms'] = struct.unpack(bsaflag + 'f', ccp4file.read(4))[0]
        header['nlabl'] = struct.unpack(bsaflag + 'I', ccp4file.read(4))[0]
        if header['nlabl']:
            binlabel = ccp4file.read(80 * header['nlabl'])
            flag = bsaflag + str(80 * header['nlabl']) + 's'
            label = struct.unpack(flag, binlabel)[0]
            header['label'] = label.decode('utf-8').rstrip('\x00')
        else:
            header['label'] = None
        ccp4file.seek(256 * 4)
        # TODO: Parse symmetry records, if any.
        return header