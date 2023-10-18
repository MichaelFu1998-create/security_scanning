def train(self, text):
        r"""Generate a probability dict from the provided text.

        Text to 0-order probability statistics as a dict

        Parameters
        ----------
        text : str
            The text data over which to calculate probability statistics. This
            must not contain the NUL (0x00) character because that is used to
            indicate the end of data.

        Example
        -------
        >>> ac = Arithmetic()
        >>> ac.train('the quick brown fox jumped over the lazy dog')
        >>> ac.get_probs()
        {' ': (Fraction(0, 1), Fraction(8, 45)),
         'o': (Fraction(8, 45), Fraction(4, 15)),
         'e': (Fraction(4, 15), Fraction(16, 45)),
         'u': (Fraction(16, 45), Fraction(2, 5)),
         't': (Fraction(2, 5), Fraction(4, 9)),
         'r': (Fraction(4, 9), Fraction(22, 45)),
         'h': (Fraction(22, 45), Fraction(8, 15)),
         'd': (Fraction(8, 15), Fraction(26, 45)),
         'z': (Fraction(26, 45), Fraction(3, 5)),
         'y': (Fraction(3, 5), Fraction(28, 45)),
         'x': (Fraction(28, 45), Fraction(29, 45)),
         'w': (Fraction(29, 45), Fraction(2, 3)),
         'v': (Fraction(2, 3), Fraction(31, 45)),
         'q': (Fraction(31, 45), Fraction(32, 45)),
         'p': (Fraction(32, 45), Fraction(11, 15)),
         'n': (Fraction(11, 15), Fraction(34, 45)),
         'm': (Fraction(34, 45), Fraction(7, 9)),
         'l': (Fraction(7, 9), Fraction(4, 5)),
         'k': (Fraction(4, 5), Fraction(37, 45)),
         'j': (Fraction(37, 45), Fraction(38, 45)),
         'i': (Fraction(38, 45), Fraction(13, 15)),
         'g': (Fraction(13, 15), Fraction(8, 9)),
         'f': (Fraction(8, 9), Fraction(41, 45)),
         'c': (Fraction(41, 45), Fraction(14, 15)),
         'b': (Fraction(14, 15), Fraction(43, 45)),
         'a': (Fraction(43, 45), Fraction(44, 45)),
         '\x00': (Fraction(44, 45), Fraction(1, 1))}

        """
        text = text_type(text)
        if '\x00' in text:
            text = text.replace('\x00', ' ')
        counts = Counter(text)
        counts['\x00'] = 1
        tot_letters = sum(counts.values())

        tot = 0
        self._probs = {}
        prev = Fraction(0)
        for char, count in sorted(
            counts.items(), key=lambda x: (x[1], x[0]), reverse=True
        ):
            follow = Fraction(tot + count, tot_letters)
            self._probs[char] = (prev, follow)
            prev = follow
            tot = tot + count