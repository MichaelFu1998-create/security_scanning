def _get_labels(self, y):
        """
        Construct pylearn2 dataset labels.

        Parameters
        ----------
        y : array_like, optional
            Labels.
        """
        y = np.asarray(y)
        assert y.ndim == 1
        # convert to one-hot
        labels = np.unique(y).tolist()
        oh = np.zeros((y.size, len(labels)), dtype=float)
        for i, label in enumerate(y):
            oh[i, labels.index(label)] = 1.
        return oh