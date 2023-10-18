def score_models(clf, X, y, encoder, runs=1):
    """
    Takes in a classifier that supports multiclass classification, and X and a y, and returns a cross validation score.

    """

    scores = []

    X_test = None
    for _ in range(runs):
        X_test = encoder().fit_transform(X, y)

        # Some models, like logistic regression, like normalized features otherwise they underperform and/or take a long time to converge.
        # To be rigorous, we should have trained the normalization on each fold individually via pipelines.
        # See grid_search_example to learn how to do it.
        X_test = StandardScaler().fit_transform(X_test)

        scores.append(cross_validate(clf, X_test, y, n_jobs=1, cv=5)['test_score'])
        gc.collect()

    scores = [y for z in [x for x in scores] for y in z]

    return float(np.mean(scores)), float(np.std(scores)), scores, X_test.shape[1]