def _expand_alternates(self, phonetic):
        """Expand phonetic alternates separated by |s.

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
            return self._normalize_lang_attrs(phonetic, False)

        prefix = phonetic[:alt_start]
        alt_start += 1  # get past the (
        alt_end = phonetic.find(')', alt_start)
        alt_string = phonetic[alt_start:alt_end]
        alt_end += 1  # get past the )
        suffix = phonetic[alt_end:]
        alt_array = alt_string.split('|')
        result = ''

        for i in range(len(alt_array)):
            alt = alt_array[i]
            alternate = self._expand_alternates(prefix + alt + suffix)
            if alternate != '' and alternate != '[0]':
                if result != '':
                    result += '|'
                result += alternate

        return result