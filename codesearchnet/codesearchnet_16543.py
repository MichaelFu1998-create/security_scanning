def _detect_byteorder(ccp4file):
        """Detect the byteorder of stream `ccp4file` and return format character.

        Try all endinaness and alignment options until we find
        something that looks sensible ("MAPS " in the first 4 bytes).

        (The ``machst`` field could be used to obtain endianness, but
        it does not specify alignment.)

        .. SeeAlso::

          :mod:`struct`
        """
        bsaflag = None
        ccp4file.seek(52 * 4)
        mapbin = ccp4file.read(4)
        for flag in '@=<>':
            mapstr = struct.unpack(flag + '4s', mapbin)[0].decode('utf-8')
            if mapstr.upper() == 'MAP ':
                bsaflag = flag
                break  # Only possible value according to spec.
        else:
            raise TypeError(
                "Cannot decode header --- corrupted or wrong format?")
        ccp4file.seek(0)
        return bsaflag