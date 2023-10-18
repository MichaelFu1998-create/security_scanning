def fit_and_score_estimator(estimator, parameters, cv, X, y=None, scoring=None,
                            iid=True, n_jobs=1, verbose=1,
                            pre_dispatch='2*n_jobs'):
    """Fit and score an estimator with cross-validation

    This function is basically a copy of sklearn's
    model_selection._BaseSearchCV._fit(), which is the core of the GridSearchCV
    fit() method. Unfortunately, that class does _not_ return the training
    set scores, which we want to save in the database, and because of the
    way it's written, you can't change it by subclassing or monkeypatching.

    This function uses some undocumented internal sklearn APIs (non-public).
    It was written against sklearn version 0.16.1. Prior Versions are likely
    to fail due to changes in the design of cross_validation module.

    Returns
    -------
    out : dict, with keys 'mean_test_score' 'test_scores', 'train_scores'
        The scores on the training and test sets, as well as the mean test set
        score.
    """

    scorer = check_scoring(estimator, scoring=scoring)
    n_samples = num_samples(X)
    X, y = check_arrays(X, y, allow_lists=True, sparse_format='csr',
                        allow_nans=True)
    if y is not None:
        if len(y) != n_samples:
            raise ValueError('Target variable (y) has a different number '
                             'of samples (%i) than data (X: %i samples)'
                             % (len(y), n_samples))
    cv = check_cv(cv=cv, y=y, classifier=is_classifier(estimator))

    out = Parallel(
        n_jobs=n_jobs, verbose=verbose, pre_dispatch=pre_dispatch
    )(
        delayed(_fit_and_score)(clone(estimator), X, y, scorer,
                                train, test, verbose, parameters,
                                fit_params=None)
        for train, test in cv.split(X, y))

    assert len(out) == cv.n_splits

    train_scores, test_scores = [], []
    n_train_samples, n_test_samples = [], []
    for test_score, n_test, train_score, n_train, _ in out:
        train_scores.append(train_score)
        test_scores.append(test_score)
        n_test_samples.append(n_test)
        n_train_samples.append(n_train)

    train_scores, test_scores = map(list, check_arrays(train_scores,
                                                       test_scores,
                                                       warn_nans=True,
                                                       replace_nans=True))

    if iid:
        if verbose > 0 and is_msmbuilder_estimator(estimator):
            print('[CV] Using MSMBuilder API n_samples averaging')
            print('[CV]   n_train_samples: %s' % str(n_train_samples))
            print('[CV]   n_test_samples: %s' % str(n_test_samples))
        mean_test_score = np.average(test_scores, weights=n_test_samples)
        mean_train_score = np.average(train_scores, weights=n_train_samples)
    else:
        mean_test_score = np.average(test_scores)
        mean_train_score = np.average(train_scores)

    grid_scores = {
        'mean_test_score': mean_test_score, 'test_scores': test_scores,
        'mean_train_score': mean_train_score, 'train_scores': train_scores,
        'n_test_samples': n_test_samples, 'n_train_samples': n_train_samples}
    return grid_scores