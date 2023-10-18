def get_checksum(cls, phrase):
        """Given a mnemonic word string, return a string of the computed checksum.

        :rtype: str
        """
        phrase_split = phrase.split(" ")
        if len(phrase_split) < 12:
            raise ValueError("Invalid mnemonic phrase")
        if len(phrase_split) > 13:
            # Standard format
            phrase = phrase_split[:24]
        else:
            # MyMonero format
            phrase = phrase_split[:12]
        wstr = "".join(word[:cls.unique_prefix_length] for word in phrase)
        wstr = bytearray(wstr.encode('utf-8'))
        z = ((crc32(wstr) & 0xffffffff) ^ 0xffffffff ) >> 0
        z2 = ((z ^ 0xffffffff) >> 0) % len(phrase)
        return phrase_split[z2]