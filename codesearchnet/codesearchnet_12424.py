def encode(cls, hex):
        """Convert hexadecimal string to mnemonic word representation with checksum.
        """
        out = []
        for i in range(len(hex) // 8):
            word = endian_swap(hex[8*i:8*i+8])
            x = int(word, 16)
            w1 = x % cls.n
            w2 = (x // cls.n + w1) % cls.n
            w3 = (x // cls.n // cls.n + w2) % cls.n
            out += [cls.word_list[w1], cls.word_list[w2], cls.word_list[w3]]
        checksum = cls.get_checksum(" ".join(out))
        out.append(checksum)
        return " ".join(out)