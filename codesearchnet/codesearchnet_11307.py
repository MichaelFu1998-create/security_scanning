def encode(self, word, max_length=4, zero_pad=True):
        """Return the Phonix code for a word.

        Parameters
        ----------
        word : str
            The word to transform
        max_length : int
            The length of the code returned (defaults to 4)
        zero_pad : bool
            Pad the end of the return value with 0s to achieve a max_length
            string

        Returns
        -------
        str
            The Phonix value

        Examples
        --------
        >>> pe = Phonix()
        >>> pe.encode('Christopher')
        'K683'
        >>> pe.encode('Niall')
        'N400'
        >>> pe.encode('Smith')
        'S530'
        >>> pe.encode('Schmidt')
        'S530'

        """

        def _start_repl(word, src, tar, post=None):
            """Replace src with tar at the start of word.

            Parameters
            ----------
            word : str
                The word to modify
            src : str
                Substring to match
            tar : str
                Substring to substitute
            post : set
                Following characters

            Returns
            -------
            str
                Modified string

            """
            if post:
                for i in post:
                    if word.startswith(src + i):
                        return tar + word[len(src) :]
            elif word.startswith(src):
                return tar + word[len(src) :]
            return word

        def _end_repl(word, src, tar, pre=None):
            """Replace src with tar at the end of word.

            Parameters
            ----------
            word : str
                The word to modify
            src : str
                Substring to match
            tar : str
                Substring to substitute
            pre : set
                Preceding characters

            Returns
            -------
            str
                Modified string

            """
            if pre:
                for i in pre:
                    if word.endswith(i + src):
                        return word[: -len(src)] + tar
            elif word.endswith(src):
                return word[: -len(src)] + tar
            return word

        def _mid_repl(word, src, tar, pre=None, post=None):
            """Replace src with tar in the middle of word.

            Parameters
            ----------
            word : str
                The word to modify
            src : str
                Substring to match
            tar : str
                Substring to substitute
            pre : set
                Preceding characters
            post : set
                Following characters

            Returns
            -------
            str
                Modified string

            """
            if pre or post:
                if not pre:
                    return word[0] + _all_repl(word[1:], src, tar, pre, post)
                elif not post:
                    return _all_repl(word[:-1], src, tar, pre, post) + word[-1]
                return _all_repl(word, src, tar, pre, post)
            return (
                word[0] + _all_repl(word[1:-1], src, tar, pre, post) + word[-1]
            )

        def _all_repl(word, src, tar, pre=None, post=None):
            """Replace src with tar anywhere in word.

            Parameters
            ----------
            word : str
                The word to modify
            src : str
                Substring to match
            tar : str
                Substring to substitute
            pre : set
                Preceding characters
            post : set
                Following characters

            Returns
            -------
            str
                Modified string

            """
            if pre or post:
                if post:
                    post = post
                else:
                    post = frozenset(('',))
                if pre:
                    pre = pre
                else:
                    pre = frozenset(('',))

                for i, j in ((i, j) for i in pre for j in post):
                    word = word.replace(i + src + j, i + tar + j)
                return word
            else:
                return word.replace(src, tar)

        repl_at = (_start_repl, _end_repl, _mid_repl, _all_repl)

        sdx = ''

        word = unicode_normalize('NFKD', text_type(word.upper()))
        word = word.replace('ß', 'SS')
        word = ''.join(c for c in word if c in self._uc_set)
        if word:
            for trans in self._substitutions:
                word = repl_at[trans[0]](word, *trans[1:])
            if word[0] in self._uc_vy_set:
                sdx = 'v' + word[1:].translate(self._trans)
            else:
                sdx = word[0] + word[1:].translate(self._trans)
            sdx = self._delete_consecutive_repeats(sdx)
            sdx = sdx.replace('0', '')

        # Clamp max_length to [4, 64]
        if max_length != -1:
            max_length = min(max(4, max_length), 64)
        else:
            max_length = 64

        if zero_pad:
            sdx += '0' * max_length
        if not sdx:
            sdx = '0'
        return sdx[:max_length]