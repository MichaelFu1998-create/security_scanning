def _language_index_from_code(self, code, name_mode):
        """Return the index value for a language code.

        This returns l_any if more than one code is specified or the code is
        out of bounds.

        Parameters
        ----------
        code : int
            The language code to interpret
        name_mode : str
            The name mode of the algorithm: ``gen`` (default),
            ``ash`` (Ashkenazi), or ``sep`` (Sephardic)

        Returns
        -------
        int
            Language code index

        """
        if code < 1 or code > sum(
            _LANG_DICT[_] for _ in BMDATA[name_mode]['languages']
        ):  # code out of range
            return L_ANY
        if (
            code & (code - 1)
        ) != 0:  # choice was more than one language; use any
            return L_ANY
        return code