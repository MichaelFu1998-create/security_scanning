def check_remove_particle(st, ind, im_change_frac=0.2, min_derr='3sig',
                          **kwargs):
    """
    Checks whether to remove particle 'ind' from state 'st'. If removing the
    particle increases the error by less than max( min_derr, change in image *
    im_change_frac), then the particle is removed.

    Parameters
    ----------
    st : :class:`peri.states.State`
        The state to check adding particles to.
    ind : Int
        The index of the particle to check to remove.
    im_change_frac : Float
        How good the change in error needs to be relative to the change in
        the difference image. Default is 0.2; i.e. if the error does not
        decrease by 20% of the change in the difference image, do not add
        the particle.
    min_derr : Float or '3sig'
        The minimal improvement in error to add a particle. Default is
        ``'3sig' = 3*st.sigma``.

    Returns
    -------
    killed : Bool
        Whether the particle was removed.
    p : Tuple
        The position of the removed particle.
    r : Tuple
        The radius of the removed particle.
    """
    # FIXME does not use the **kwargs, but needs b/c called with wrong kwargs
    if min_derr == '3sig':
        min_derr = 3 * st.sigma
    present_err = st.error
    present_d = st.residuals.copy()
    p, r = st.obj_remove_particle(ind)
    p = p[0]
    r = r[0]
    absent_err = st.error
    absent_d = st.residuals.copy()

    if should_particle_exist(absent_err, present_err, absent_d, present_d,
                             im_change_frac=im_change_frac, min_derr=min_derr):
        st.obj_add_particle(p, r)
        killed = False
    else:
        killed = True
    return killed, tuple(p), (r,)