def _get_dataset(self, X, y=None):
        """
        Construct a pylearn2 dataset.

        Parameters
        ----------
        X : array_like
            Training examples.
        y : array_like, optional
            Labels.
        """
        from pylearn2.datasets import DenseDesignMatrix

        X = np.asarray(X)
        assert X.ndim > 1
        if y is not None:
            y = self._get_labels(y)
        if X.ndim == 2:
            return DenseDesignMatrix(X=X, y=y)
        return DenseDesignMatrix(topo_view=X, y=y)