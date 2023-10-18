def _get_labels(self, y):
        """
        Construct pylearn2 dataset labels.

        Parameters
        ----------
        y : array_like, optional
            Labels.
        """
        y = np.asarray(y)
        if y.ndim == 1:
            return y.reshape((y.size, 1))
        assert y.ndim == 2
        return y