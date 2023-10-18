def _core_computation(X_train, X_test, inbag, pred_centered, n_trees,
                      memory_constrained=False, memory_limit=None,
                      test_mode=False):
    """
    Helper function, that performs the core computation

    Parameters
    ----------
    X_train : ndarray
        An array with shape (n_train_sample, n_features).

    X_test : ndarray
        An array with shape (n_test_sample, n_features).

    inbag : ndarray
        The inbag matrix that fit the data. If set to `None` (default) it
        will be inferred from the forest. However, this only works for trees
        for which bootstrapping was set to `True`. That is, if sampling was
        done with replacement. Otherwise, users need to provide their own
        inbag matrix.

    pred_centered : ndarray
        Centered predictions that are an intermediate result in the
        computation.

    memory_constrained: boolean (optional)
        Whether or not there is a restriction on memory. If False, it is
        assumed that a ndarry of shape (n_train_sample,n_test_sample) fits
        in main memory. Setting to True can actually provide a speed up if
        memory_limit is tuned to the optimal range.

    memory_limit: int (optional)
        An upper bound for how much memory the itermediate matrices will take
        up in Megabytes. This must be provided if memory_constrained=True.


    """
    if not memory_constrained:
        return np.sum((np.dot(inbag - 1, pred_centered.T) / n_trees) ** 2, 0)

    if not memory_limit:
        raise ValueError('If memory_constrained=True, must provide',
                         'memory_limit.')

    # Assumes double precision float
    chunk_size = int((memory_limit * 1e6) / (8.0 * X_train.shape[0]))

    if chunk_size == 0:
        min_limit = 8.0 * X_train.shape[0] / 1e6
        raise ValueError('memory_limit provided is too small.' +
                         'For these dimensions, memory_limit must ' +
                         'be greater than or equal to %.3e' % min_limit)

    chunk_edges = np.arange(0, X_test.shape[0] + chunk_size, chunk_size)
    inds = range(X_test.shape[0])
    chunks = [inds[chunk_edges[i]:chunk_edges[i+1]]
              for i in range(len(chunk_edges)-1)]
    if test_mode:
        print('Number of chunks: %d' % (len(chunks),))
    V_IJ = np.concatenate([
                np.sum((np.dot(inbag-1, pred_centered[chunk].T)/n_trees)**2, 0)
                for chunk in chunks])
    return V_IJ