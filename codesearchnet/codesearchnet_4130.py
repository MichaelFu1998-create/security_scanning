def gen_model(clf, arr, sel_score):
    """
    Fits a classifier to data and a target score
    clf is an input classifier that implements the fit method.
    arr is a data array(X)
    sel_score is the target list (y) where y[n] corresponds to X[n,:]
    sim_fit is not a useful return value.  Instead the clf is the useful output.
    """
    set_score = numpy.asarray(sel_score, dtype=numpy.int)
    sim_fit = clf.fit(arr, set_score)
    return(sim_fit)