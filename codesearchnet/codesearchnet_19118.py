def _get_rhos(X, indices, Ks, max_K, save_all_Ks, min_dist):
    "Gets within-bag distances for each bag."
    logger.info("Getting within-bag distances...")

    if max_K >= X.n_pts.min():
        msg = "asked for K = {}, but there's a bag with only {} points"
        raise ValueError(msg.format(max_K, X.n_pts.min()))

    # need to throw away the closest neighbor, which will always be self
    # thus K=1 corresponds to column 1 in the result array
    which_Ks = slice(1, None) if save_all_Ks else Ks

    indices = plog(indices, name="within-bag distances")
    rhos = [None] * len(X)
    for i, (idx, bag) in enumerate(zip(indices, X)):
        r = np.sqrt(idx.nn_index(bag, max_K + 1)[1][:, which_Ks])
        np.maximum(min_dist, r, out=r)
        rhos[i] = r
    return rhos