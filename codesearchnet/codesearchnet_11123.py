def decode(self, code, terminator='\0'):
        r"""Return a word decoded from BWT form.

        Parameters
        ----------
        code : str
            The word to transform from BWT form
        terminator : str
            A character added to signal the end of the string

        Returns
        -------
        str
            Word decoded by BWT

        Raises
        ------
        ValueError
            Specified terminator absent from code.

        Examples
        --------
        >>> bwt = BWT()
        >>> bwt.decode('n\x00ilag')
        'align'
        >>> bwt.decode('annb\x00aa')
        'banana'
        >>> bwt.decode('annb@aa', '@')
        'banana'

        """
        if code:
            if terminator not in code:
                raise ValueError(
                    'Specified terminator, {}, absent from code.'.format(
                        terminator if terminator != '\0' else '\\0'
                    )
                )
            else:
                wordlist = [''] * len(code)
                for i in range(len(code)):
                    wordlist = sorted(
                        code[i] + wordlist[i] for i in range(len(code))
                    )
                rows = [w for w in wordlist if w[-1] == terminator][0]
                return rows.rstrip(terminator)
        else:
            return ''