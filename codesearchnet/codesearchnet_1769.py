def shuffle(self, x, random=None):
        """x, random=random.random -> shuffle list x in place; return None.

        Optional arg random is a 0-argument function returning a random
        float in [0.0, 1.0); by default, the standard random.random.

        """

        if random is None:
            random = self.random
        _int = int
        for i in reversed(xrange(1, len(x))):
            # pick an element in x[:i+1] with which to exchange x[i]
            j = _int(random() * (i+1))
            x[i], x[j] = x[j], x[i]