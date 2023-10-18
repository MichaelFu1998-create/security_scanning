def check_add_particles(st, guess, rad='calc', do_opt=True, im_change_frac=0.2,
                        min_derr='3sig', **kwargs):
    """
    Checks whether to add particles at a given position by seeing if adding
    the particle improves the fit of the state.

    Parameters
    ----------
    st : :class:`peri.states.State`
        The state to check adding particles to.
    guess : [N,3] list-like
        The positions of particles to check to add.
    rad : {Float, ``'calc'``}, optional.
        The radius of the newly-added particles. Default is ``'calc'``,
        which uses the states current radii's median.
    do_opt : Bool, optional
        Whether to optimize the particle position before checking if it
        should be kept. Default is True (optimizes position).
    im_change_frac : Float
        How good the change in error needs to be relative to the change in
        the difference image. Default is 0.2; i.e. if the error does not
        decrease by 20% of the change in the difference image, do not add
        the particle.
    min_derr : Float or '3sig'
        The minimal improvement in error to add a particle. Default
        is ``'3sig' = 3*st.sigma``.

    Returns
    -------
    accepts : Int
        The number of added particles
    new_poses : [N,3] list
        List of the positions of the added particles. If ``do_opt==True``,
        then these positions will differ from the input 'guess'.
    """
    # FIXME does not use the **kwargs, but needs b/c called with wrong kwargs
    if min_derr == '3sig':
        min_derr = 3 * st.sigma
    accepts = 0
    new_poses = []
    if rad == 'calc':
        rad = guess_add_radii(st)
    message = ('-'*30 + 'ADDING' + '-'*30 +
               '\n  Z\t  Y\t  X\t  R\t|\t ERR0\t\t ERR1')
    with log.noformat():
        CLOG.info(message)
    for a in range(guess.shape[0]):
        p0 = guess[a]
        absent_err = st.error
        absent_d = st.residuals.copy()
        ind = st.obj_add_particle(p0, rad)
        if do_opt:
            # the slowest part of this
            opt.do_levmarq_particles(
                st, ind, damping=1.0, max_iter=1, run_length=3,
                eig_update=False, include_rad=False)
        present_err = st.error
        present_d = st.residuals.copy()
        dont_kill = should_particle_exist(
                absent_err, present_err, absent_d, present_d,
                im_change_frac=im_change_frac, min_derr=min_derr)
        if dont_kill:
            accepts += 1
            p = tuple(st.obj_get_positions()[ind].ravel())
            r = tuple(st.obj_get_radii()[ind].ravel())
            new_poses.append(p)
            part_msg = '%2.2f\t%3.2f\t%3.2f\t%3.2f\t|\t%4.3f  \t%4.3f' % (
                    p + r + (absent_err, st.error))
            with log.noformat():
                CLOG.info(part_msg)
        else:
            st.obj_remove_particle(ind)
            if np.abs(absent_err - st.error) > 1e-4:
                raise RuntimeError('updates not exact?')
    return accepts, new_poses