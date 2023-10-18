def transform(self, X):
        '''
        Transform a list of bag features into its projection series
        representation.

        Parameters
        ----------
        X : :class:`skl_groups.features.Features` or list of bag feature arrays
            New data to transform. The data should all lie in [0, 1];
            use :class:`skl_groups.preprocessing.BagMinMaxScaler` if not.

        Returns
        -------
        X_new : integer array, shape ``[len(X), dim_]``
            X transformed into the new space.
        '''
        self._check_fitted()
        M = self.smoothness
        dim = self.dim_
        inds = self.inds_
        do_check = self.do_bounds_check

        X = as_features(X)
        if X.dim != dim:
            msg = "model fit for dimension {} but got dim {}"
            raise ValueError(msg.format(dim, X.dim))

        Xt = np.empty((len(X), self.inds_.shape[0]))
        Xt.fill(np.nan)

        if self.basis == 'cosine':  # TODO: put this in a C extension?
            coefs = (np.pi * np.arange(M + 1))[..., :]
            for i, bag in enumerate(X):
                if do_check:
                    if np.min(bag) < 0 or np.max(bag) > 1:
                        raise ValueError("Bag {} not in [0, 1]".format(i))

                # apply each phi func to each dataset point: n x dim x M
                phi = coefs * bag[..., np.newaxis]
                np.cos(phi, out=phi)
                phi[:, :, 1:] *= np.sqrt(2)

                # B is the evaluation of each tensor-prodded basis func
                # at each point: n x inds.shape[0]
                B = reduce(op.mul, (phi[:, i, inds[:, i]] for i in xrange(dim)))

                Xt[i, :] = np.mean(B, axis=0)
        else:
            raise ValueError("unknown basis '{}'".format(self.basis))

        return Xt