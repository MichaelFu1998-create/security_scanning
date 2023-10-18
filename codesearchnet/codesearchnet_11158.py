def _remove_dupes(self, phonetic):
        """Remove duplicates from a phonetic encoding list.

        Parameters
        ----------
        phonetic : str
            A Beider-Morse phonetic encoding

        Returns
        -------
        str
            A Beider-Morse phonetic code

        """
        alt_string = phonetic
        alt_array = alt_string.split('|')

        result = '|'
        for i in range(len(alt_array)):
            alt = alt_array[i]
            if alt and '|' + alt + '|' not in result:
                result += alt + '|'

        return result[1:-1]