def _phonetic_numbers(self, phonetic):
        """Prepare & join phonetic numbers.

        Split phonetic value on '-', run through _pnums_with_leading_space,
        and join with ' '

        Parameters
        ----------
        phonetic : str
            A Beider-Morse phonetic encoding

        Returns
        -------
        str
            A Beider-Morse phonetic code

        """
        phonetic_array = phonetic.split('-')  # for names with spaces in them
        result = ' '.join(
            [self._pnums_with_leading_space(i)[1:] for i in phonetic_array]
        )
        return result