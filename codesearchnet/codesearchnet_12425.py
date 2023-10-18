def decode(cls, phrase):
        """Calculate hexadecimal representation of the phrase.
        """
        phrase = phrase.split(" ")
        out = ""
        for i in range(len(phrase) // 3):
            word1, word2, word3 = phrase[3*i:3*i+3]
            w1 = cls.word_list.index(word1)
            w2 = cls.word_list.index(word2) % cls.n
            w3 = cls.word_list.index(word3) % cls.n
            x = w1 + cls.n *((w2 - w1) % cls.n) + cls.n * cls.n * ((w3 - w2) % cls.n)
            out += endian_swap("%08x" % x)
        return out