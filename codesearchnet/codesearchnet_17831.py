def feature_guess(st, rad, invert='guess', minmass=None, use_tp=False,
                  trim_edge=False, **kwargs):
    """
    Makes a guess at particle positions using heuristic centroid methods.

    Parameters
    ----------
    st : :class:`peri.states.State`
        The state to check adding particles to.
    rad : Float
        The feature size for featuring.
    invert : {'guess', True, False}, optional
        Whether to invert the image; set to True for there are dark
        particles on a bright background, False for bright particles.
        The default is to guess from the state's current particles.
    minmass : Float or None, optional
        The minimum mass/masscut of a particle. Default is ``None`` =
        calculated internally.
    use_tp : Bool, optional
        Whether or not to use trackpy. Default is ``False``, since trackpy
        cuts out particles at the edge.
    trim_edge : Bool, optional
        Whether to trim particles at the edge pixels of the image. Can be
        useful for initial featuring but is bad for adding missing particles
        as they are frequently at the edge. Default is ``False``.

    Returns
    -------
    guess : [N,3] numpy.ndarray
        The featured positions of the particles, sorted in order of decreasing
        feature mass.
    npart : Int
        The number of added particles.
    """
    # FIXME does not use the **kwargs, but needs b/c called with wrong kwargs
    if invert == 'guess':
        invert = guess_invert(st)
    if invert:
        im = 1 - st.residuals
    else:
        im = st.residuals
    return _feature_guess(im, rad, minmass=minmass, use_tp=use_tp,
                          trim_edge=trim_edge)