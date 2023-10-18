def fit(self, x, y=None):
        """Compute the header.
        """
        x = iter2array(x, dtype=(MoleculeContainer, CGRContainer))

        if self.__head_less:
            warn(f'{self.__class__.__name__} configured to head less mode. fit unusable')
            return self

        self._reset()
        self.__prepare(x)
        return self