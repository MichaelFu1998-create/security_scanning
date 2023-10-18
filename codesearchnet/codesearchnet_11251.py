def decode(self, text):
        r"""Perform decoding of run-length-encoding (RLE).

        Parameters
        ----------
        text : str
            A text string to decode

        Returns
        -------
        str
            Word decoded by RLE

        Examples
        --------
        >>> rle = RLE()
        >>> bwt = BWT()
        >>> bwt.decode(rle.decode('n\x00ilag'))
        'align'
        >>> rle.decode('align')
        'align'

        >>> bwt.decode(rle.decode('annb\x00aa'))
        'banana'
        >>> rle.decode('banana')
        'banana'

        >>> bwt.decode(rle.decode('ab\x00abbab5a'))
        'aaabaabababa'
        >>> rle.decode('3abaabababa')
        'aaabaabababa'

        """
        mult = ''
        decoded = []
        for letter in list(text):
            if not letter.isdigit():
                if mult:
                    decoded.append(int(mult) * letter)
                    mult = ''
                else:
                    decoded.append(letter)
            else:
                mult += letter

        text = ''.join(decoded)
        return text