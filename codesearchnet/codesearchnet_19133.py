def fit(self, X, y=None, get_rhos=False):
        '''
        Sets up for divergence estimation "from" new data "to" X.
        Builds FLANN indices for each bag, and maybe gets within-bag distances.

        Parameters
        ----------
        X : list of arrays or :class:`skl_groups.features.Features`
            The bags to search "to".

        get_rhos : boolean, optional, default False
            Compute within-bag distances :attr:`rhos_`. These are only needed
            for some divergence functions or if do_sym is passed, and they'll
            be computed (and saved) during :meth:`transform` if they're not
            computed here.

            If you're using Jensen-Shannon divergence, a higher max_K may
            be needed once it sees the number of points in the transformed bags,
            so the computation here might be wasted.
        '''
        self.features_ = X = as_features(X, stack=True, bare=True)

        # if we're using a function that needs to pick its K vals itself,
        # then we need to set max_K here. when we transform(), might have to
        # re-do this :|
        Ks = self._get_Ks()
        _, _, _, max_K, save_all_Ks, _ = _choose_funcs(
            self.div_funcs, Ks, X.dim, X.n_pts, None, self.version)

        if max_K >= X.n_pts.min():
            msg = "asked for K = {}, but there's a bag with only {} points"
            raise ValueError(msg.format(max_K, X.n_pts.min()))

        memory = self.memory
        if isinstance(memory, string_types):
            memory = Memory(cachedir=memory, verbose=0)

        self.indices_ = id = memory.cache(_build_indices)(X, self._flann_args())
        if get_rhos:
            self.rhos_ = _get_rhos(X, id, Ks, max_K, save_all_Ks, self.min_dist)
        elif hasattr(self, 'rhos_'):
            del self.rhos_
        return self