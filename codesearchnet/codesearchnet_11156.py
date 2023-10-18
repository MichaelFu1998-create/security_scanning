def _pnums_with_leading_space(self, phonetic):
        """Join prefixes & suffixes in cases of alternate phonetic values.

        Parameters
        ----------
        phonetic : str
            A Beider-Morse phonetic encoding

        Returns
        -------
        str
            A Beider-Morse phonetic code

        """
        alt_start = phonetic.find('(')
        if alt_start == -1:
            return ' ' + self._phonetic_number(phonetic)

        prefix = phonetic[:alt_start]
        alt_start += 1  # get past the (
        alt_end = phonetic.find(')', alt_start)
        alt_string = phonetic[alt_start:alt_end]
        alt_end += 1  # get past the )
        suffix = phonetic[alt_end:]
        alt_array = alt_string.split('|')
        result = ''
        for alt in alt_array:
            result += self._pnums_with_leading_space(prefix + alt + suffix)

        return result