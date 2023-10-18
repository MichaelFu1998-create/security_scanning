def seed(self, a=None):
        """Initialize internal state of the random number generator.

        None or no argument seeds from current time or from an operating
        system specific randomness source if available.

        If a is not None or is an int or long, hash(a) is used instead.
        Hash values for some types are nondeterministic when the
        PYTHONHASHSEED environment variable is enabled.
        """

        super(Random, self).seed(a)
        self.gauss_next = None