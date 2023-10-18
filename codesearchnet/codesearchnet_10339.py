def load(self, filename, append=False):
        """Load collection from pickled file *filename*.

        *append* determines if the saved collection is added to the current one
        or if it replaces the current content.

        If no extension is provided, ".collection" is appended.
        """
        tmp = cPickle.load(open(self._canonicalize(filename), 'rb'))
        if append:
            self.extend(tmp)
        else:
            self[:] = tmp[:]
        del tmp