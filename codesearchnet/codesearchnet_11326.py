def dist(
        self,
        src,
        tar,
        word_approx_min=0.3,
        char_approx_min=0.73,
        tests=2 ** 12 - 1,
    ):
        """Return the normalized Synoname distance between two words.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        word_approx_min : float
            The minimum word approximation value to signal a 'word_approx'
            match
        char_approx_min : float
            The minimum character approximation value to signal a 'char_approx'
            match
        tests : int or Iterable
            Either an integer indicating tests to perform or a list of test
            names to perform (defaults to performing all tests)

        Returns
        -------
        float
            Normalized Synoname distance

        """
        return (
            synoname(src, tar, word_approx_min, char_approx_min, tests, False)
            / 14
        )