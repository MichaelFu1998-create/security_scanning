def transform(self, X):
        r'''
        Computes the divergences from X to :attr:`features_`.

        Parameters
        ----------
        X : list of bag feature arrays or :class:`skl_groups.features.Features`
            The bags to search "from".

        Returns
        -------
        divs : array of shape ``[len(div_funcs), len(Ks), len(X), len(features_)] + ([2] if do_sym else [])``
            The divergences from X to :attr:`features_`.
            ``divs[d, k, i, j]`` is the ``div_funcs[d]`` divergence
            from ``X[i]`` to ``fetaures_[j]`` using a K of ``Ks[k]``.
            If ``do_sym``, ``divs[d, k, i, j, 0]`` is
            :math:`D_{d,k}( X_i \| \texttt{features_}_j)` and
            ``divs[d, k, i, j, 1]`` is :math:`D_{d,k}(\texttt{features_}_j \| X_i)`.
        '''
        X = as_features(X, stack=True, bare=True)
        Y = self.features_

        Ks = np.asarray(self.Ks)

        if X.dim != Y.dim:
            msg = "incompatible dimensions: fit with {}, transform with {}"
            raise ValueError(msg.format(Y.dim, X.dim))

        memory = self.memory
        if isinstance(memory, string_types):
            memory = Memory(cachedir=memory, verbose=0)

        # ignore Y_indices to avoid slow pickling of them
        # NOTE: if the indices are approximate, then might not get the same
        #       results!
        est = memory.cache(_est_divs, ignore=['n_jobs', 'Y_indices', 'Y_rhos'])
        output, self.rhos_ = est(
            X, Y, self.indices_, getattr(self, 'rhos_', None),
            self.div_funcs, Ks,
            self.do_sym, self.clamp, self.version, self.min_dist,
            self._flann_args(), self._n_jobs)
        return output