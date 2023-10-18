def encode(self, word, terminator='\0'):
        r"""Return the Burrows-Wheeler transformed form of a word.

        Parameters
        ----------
        word : str
            The word to transform using BWT
        terminator : str
            A character added to signal the end of the string

        Returns
        -------
        str
            Word encoded by BWT

        Raises
        ------
        ValueError
            Specified terminator absent from code.

        Examples
        --------
        >>> bwt = BWT()
        >>> bwt.encode('align')
        'n\x00ilag'
        >>> bwt.encode('banana')
        'annb\x00aa'
        >>> bwt.encode('banana', '@')
        'annb@aa'

        """
        if word:
            if terminator in word:
                raise ValueError(
                    'Specified terminator, {}, already in word.'.format(
                        terminator if terminator != '\0' else '\\0'
                    )
                )
            else:
                word += terminator
                wordlist = sorted(
                    word[i:] + word[:i] for i in range(len(word))
                )
                return ''.join([w[-1] for w in wordlist])
        else:
            return terminator