def remove_bad_particles(st, min_rad='calc', max_rad='calc', min_edge_dist=2.0,
                         check_rad_cutoff=[3.5, 15], check_outside_im=True,
                         tries=50, im_change_frac=0.2, **kwargs):
    """
    Removes improperly-featured particles from the state, based on a
    combination of particle size and the change in error on removal.

    Parameters
    -----------
    st : :class:`peri.states.State`
        The state to remove bad particles from.
    min_rad : Float, optional
        All particles with radius below min_rad are automatically deleted.
        Set to 'calc' to make it the median rad - 25* radius std.
        Default is 'calc'.

    max_rad : Float, optional
        All particles with radius above max_rad are automatically deleted.
        Set to 'calc' to make it the median rad + 15* radius std.
        Default is 'calc'.

    min_edge_dist : Float, optional
        All particles within min_edge_dist of the (padded) image
        edges are automatically deleted. Default is 2.0

    check_rad_cutoff : 2-element list of floats, optional
        Particles with radii < check_rad_cutoff[0] or > check_rad_cutoff[1]
        are checked if they should be deleted. Set to 'calc' to make it the
        median rad +- 3.5 * radius std. Default is [3.5, 15].

    check_outside_im : Bool, optional
        If True, checks if particles located outside the unpadded image
        should be deleted. Default is True.

    tries : Int, optional
        The maximum number of particles with radii < check_rad_cutoff
        to try to remove. Checks in increasing order of radius size.
        Default is 50.

    im_change_frac : Float, , optional
        Number between 0 and 1. If removing a particle decreases the
        error by less than im_change_frac*the change in the image, then
        the particle is deleted. Default is 0.2

    Returns
    -------
    removed: Int
        The cumulative number of particles removed.
    """
    is_near_im_edge = lambda pos, pad: (((pos + st.pad) < pad) | (pos >
            np.array(st.ishape.shape) + st.pad - pad)).any(axis=1)
    # returns True if the position is within 'pad' of the _outer_ image edge
    removed = 0
    attempts = 0

    n_tot_part = st.obj_get_positions().shape[0]
    q10 = int(0.1 * n_tot_part)  # 10% quartile
    r_sig = np.sort(st.obj_get_radii())[q10:-q10].std()
    r_med = np.median(st.obj_get_radii())
    if max_rad == 'calc':
        max_rad = r_med + 15*r_sig
    if min_rad == 'calc':
        min_rad = r_med - 25*r_sig
    if check_rad_cutoff == 'calc':
        check_rad_cutoff = [r_med - 7.5*r_sig, r_med + 7.5*r_sig]

    # 1. Automatic deletion:
    rad_wrong_size = np.nonzero(
            (st.obj_get_radii() < min_rad) | (st.obj_get_radii() > max_rad))[0]
    near_im_edge = np.nonzero(is_near_im_edge(st.obj_get_positions(),
                              min_edge_dist - st.pad))[0]
    delete_inds = np.unique(np.append(rad_wrong_size, near_im_edge)).tolist()
    delete_poses = st.obj_get_positions()[delete_inds].tolist()
    message = ('-'*27 + 'SUBTRACTING' + '-'*28 +
               '\n  Z\t  Y\t  X\t  R\t|\t ERR0\t\t ERR1')
    with log.noformat():
        CLOG.info(message)

    for pos in delete_poses:
        ind = st.obj_closest_particle(pos)
        old_err = st.error
        p, r = st.obj_remove_particle(ind)
        p = p[0]
        r = r[0]
        part_msg = '%2.2f\t%3.2f\t%3.2f\t%3.2f\t|\t%4.3f  \t%4.3f' % (
                tuple(p) + (r,) + (old_err, st.error))
        with log.noformat():
            CLOG.info(part_msg)
        removed += 1

    # 2. Conditional deletion:
    check_rad_inds = np.nonzero((st.obj_get_radii() < check_rad_cutoff[0]) |
                                (st.obj_get_radii() > check_rad_cutoff[1]))[0]
    if check_outside_im:
        check_edge_inds = np.nonzero(
            is_near_im_edge(st.obj_get_positions(), st.pad))[0]
        check_inds = np.unique(np.append(check_rad_inds, check_edge_inds))
    else:
        check_inds = check_rad_inds

    check_inds = check_inds[np.argsort(st.obj_get_radii()[check_inds])]
    tries = np.min([tries, check_inds.size])
    check_poses = st.obj_get_positions()[check_inds[:tries]].copy()
    for pos in check_poses:
        old_err = st.error
        ind = st.obj_closest_particle(pos)
        killed, p, r = check_remove_particle(
            st, ind, im_change_frac=im_change_frac)
        if killed:
            removed += 1
            check_inds[check_inds > ind] -= 1  # cleaning up indices....
            delete_poses.append(pos)
            part_msg = '%2.2f\t%3.2f\t%3.2f\t%3.2f\t|\t%4.3f  \t%4.3f' % (
                    p + r + (old_err, st.error))
            with log.noformat():
                CLOG.info(part_msg)
    return removed, delete_poses