def encode(self, text):
        r"""Perform encoding of run-length-encoding (RLE).

        Parameters
        ----------
        text : str
            A text string to encode

        Returns
        -------
        str
            Word decoded by RLE

        Examples
        --------
        >>> rle = RLE()
        >>> bwt = BWT()
        >>> rle.encode(bwt.encode('align'))
        'n\x00ilag'
        >>> rle.encode('align')
        'align'

        >>> rle.encode(bwt.encode('banana'))
        'annb\x00aa'
        >>> rle.encode('banana')
        'banana'

        >>> rle.encode(bwt.encode('aaabaabababa'))
        'ab\x00abbab5a'
        >>> rle.encode('aaabaabababa')
        '3abaabababa'

        """
        if text:
            text = ((len(list(g)), k) for k, g in groupby(text))
            text = (
                (str(n) + k if n > 2 else (k if n == 1 else 2 * k))
                for n, k in text
            )
        return ''.join(text)