def crb(self, params=None, *args, **kwargs):
        """
        Calculate the diagonal elements of the minimum covariance of the model
        with respect to parameters params. ``*args`` and ``**kwargs`` go to
        ``fisherinformation``.
        """
        fish = self.fisherinformation(params=params, *args, **kwargs)
        return np.sqrt(np.diag(np.linalg.inv(fish))) * self.sigma