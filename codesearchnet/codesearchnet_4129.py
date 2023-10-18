def gen_cv_preds(clf, arr, sel_score, num_chunks=3):
    """
    Generates cross validated predictions using an input classifier and data.
    clf is a classifier that implements that implements the fit and predict methods.
    arr is the input data array (X)
    sel_score is the target list (y).  y[n] corresponds to X[n,:]
    num_chunks is the number of cross validation folds to use
    Returns an array of the predictions where prediction[n] corresponds to X[n,:]
    """
    cv_len = int(math.floor(len(sel_score) / num_chunks))
    chunks = []
    for i in range(0, num_chunks):
        range_min = i * cv_len
        range_max = ((i + 1) * cv_len)
        if i == num_chunks - 1:
            range_max = len(sel_score)
        chunks.append(range(range_min, range_max))
    preds = []
    set_score = numpy.asarray(sel_score, dtype=numpy.int)
    chunk_vec = numpy.asarray(range(0, len(chunks)))
    for i in xrange(0, len(chunks)):
        loop_inds = list(
            chain.from_iterable([chunks[int(z)] for z, m in enumerate(range(0, len(chunks))) if int(z) != i]))
        sim_fit = clf.fit(arr[loop_inds], set_score[loop_inds])
        preds.append(list(sim_fit.predict(arr[chunks[i]])))
    all_preds = list(chain(*preds))
    return(all_preds)