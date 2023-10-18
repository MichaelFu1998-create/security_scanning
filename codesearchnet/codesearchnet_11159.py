def _normalize_lang_attrs(self, text, strip):
        """Remove embedded bracketed attributes.

        This (potentially) bitwise-ands bracketed attributes together and adds
        to the end.
        This is applied to a single alternative at a time -- not to a
        parenthesized list.
        It removes all embedded bracketed attributes, logically-ands them
        together, and places them at the end.
        However if strip is true, this can indeed remove embedded bracketed
        attributes from a parenthesized list.

        Parameters
        ----------
        text : str
            A Beider-Morse phonetic encoding (in progress)
        strip : bool
            Remove the bracketed attributes (and throw away)

        Returns
        -------
        str
            A Beider-Morse phonetic code

        Raises
        ------
        ValueError
            No closing square bracket

        """
        uninitialized = -1  # all 1's
        attrib = uninitialized
        while '[' in text:
            bracket_start = text.find('[')
            bracket_end = text.find(']', bracket_start)
            if bracket_end == -1:
                raise ValueError(
                    'No closing square bracket: text=('
                    + text
                    + ') strip=('
                    + text_type(strip)
                    + ')'
                )
            attrib &= int(text[bracket_start + 1 : bracket_end])
            text = text[:bracket_start] + text[bracket_end + 1 :]

        if attrib == uninitialized or strip:
            return text
        elif attrib == 0:
            # means that the attributes were incompatible and there is no
            # alternative here
            return '[0]'
        return text + '[' + str(attrib) + ']'