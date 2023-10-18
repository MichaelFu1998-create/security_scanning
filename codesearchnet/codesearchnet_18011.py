def get_rand_Japprox(s, params, num_inds=1000, include_cost=False, **kwargs):
    """
    Calculates a random approximation to J by returning J only at a
    set of random pixel/voxel locations.

    Parameters
    ----------
        s : :class:`peri.states.State`
            The state to calculate J for.
        params : List
            The list of parameter names to calculate the gradient of.
        num_inds : Int, optional.
            The number of pix/voxels at which to calculate the random
            approximation to J. Default is 1000.
        include_cost : Bool, optional
            Set to True to append a finite-difference measure of the full
            cost gradient onto the returned J.

    Other Parameters
    ----------------
        All kwargs parameters get passed to s.gradmodel only.

    Returns
    -------
        J : numpy.ndarray
            [d, num_inds] array of J, at the given indices.

        return_inds : numpy.ndarray or slice
            [num_inds] element array or slice(0, None) of the model
            indices at which J was evaluated.
    """
    start_time = time.time()
    tot_pix = s.residuals.size
    if num_inds < tot_pix:
        inds = np.random.choice(tot_pix, size=num_inds, replace=False)
        slicer = None
        return_inds = np.sort(inds)
    else:
        inds = None
        return_inds = slice(0, None)
        slicer = [slice(0, None)]*len(s.residuals.shape)
    if include_cost:
        Jact, ge = s.gradmodel_e(params=params, inds=inds, slicer=slicer,flat=False,
                **kwargs)
        Jact *= -1
        J = [Jact, ge]
    else:
        J = -s.gradmodel(params=params, inds=inds, slicer=slicer, flat=False,
                **kwargs)
    CLOG.debug('J:\t%f' % (time.time()-start_time))
    return J, return_inds