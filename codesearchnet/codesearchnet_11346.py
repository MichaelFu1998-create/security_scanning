def dist_abs(
        self, src, tar, weights='exponential', max_length=8, normalized=False
    ):
        """Calculate the distance between the Eudex hashes of two terms.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        weights : str, iterable, or generator function
            The weights or weights generator function

                - If set to ``None``, a simple Hamming distance is calculated.
                - If set to ``exponential``, weight decays by powers of 2, as
                  proposed in the eudex specification:
                  https://github.com/ticki/eudex.
                - If set to ``fibonacci``, weight decays through the Fibonacci
                  series, as in the eudex reference implementation.
                - If set to a callable function, this assumes it creates a
                  generator and the generator is used to populate a series of
                  weights.
                - If set to an iterable, the iterable's values should be
                  integers and will be used as the weights.

        max_length : int
            The number of characters to encode as a eudex hash
        normalized : bool
            Normalizes to [0, 1] if True

        Returns
        -------
        int
            The Eudex Hamming distance

        Examples
        --------
        >>> cmp = Eudex()
        >>> cmp.dist_abs('cat', 'hat')
        128
        >>> cmp.dist_abs('Niall', 'Neil')
        2
        >>> cmp.dist_abs('Colin', 'Cuilen')
        10
        >>> cmp.dist_abs('ATCG', 'TAGC')
        403

        >>> cmp.dist_abs('cat', 'hat', weights='fibonacci')
        34
        >>> cmp.dist_abs('Niall', 'Neil', weights='fibonacci')
        2
        >>> cmp.dist_abs('Colin', 'Cuilen', weights='fibonacci')
        7
        >>> cmp.dist_abs('ATCG', 'TAGC', weights='fibonacci')
        117

        >>> cmp.dist_abs('cat', 'hat', weights=None)
        1
        >>> cmp.dist_abs('Niall', 'Neil', weights=None)
        1
        >>> cmp.dist_abs('Colin', 'Cuilen', weights=None)
        2
        >>> cmp.dist_abs('ATCG', 'TAGC', weights=None)
        9

        >>> # Using the OEIS A000142:
        >>> cmp.dist_abs('cat', 'hat', [1, 1, 2, 6, 24, 120, 720, 5040])
        1
        >>> cmp.dist_abs('Niall', 'Neil', [1, 1, 2, 6, 24, 120, 720, 5040])
        720
        >>> cmp.dist_abs('Colin', 'Cuilen',
        ... [1, 1, 2, 6, 24, 120, 720, 5040])
        744
        >>> cmp.dist_abs('ATCG', 'TAGC', [1, 1, 2, 6, 24, 120, 720, 5040])
        6243

        """
        # Calculate the eudex hashes and XOR them
        xored = eudex(src, max_length=max_length) ^ eudex(
            tar, max_length=max_length
        )

        # Simple hamming distance (all bits are equal)
        if not weights:
            binary = bin(xored)
            distance = binary.count('1')
            if normalized:
                return distance / (len(binary) - 2)
            return distance

        # If weights is a function, it should create a generator,
        # which we now use to populate a list
        if callable(weights):
            weights = weights()
        elif weights == 'exponential':
            weights = Eudex.gen_exponential()
        elif weights == 'fibonacci':
            weights = Eudex.gen_fibonacci()
        if isinstance(weights, GeneratorType):
            weights = [next(weights) for _ in range(max_length)][::-1]

        # Sum the weighted hamming distance
        distance = 0
        max_distance = 0
        while (xored or normalized) and weights:
            max_distance += 8 * weights[-1]
            distance += bin(xored & 0xFF).count('1') * weights.pop()
            xored >>= 8

        if normalized:
            distance /= max_distance

        return distance