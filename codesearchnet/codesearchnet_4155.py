def get_algorithms(algorithm):
    """
    Gets two classifiers for each type of algorithm, and returns them.  First for predicting, second for cv error.
    type - one of util_functions.AlgorithmTypes
    """
    if algorithm == util_functions.AlgorithmTypes.classification:
        clf = sklearn.ensemble.GradientBoostingClassifier(n_estimators=100, learn_rate=.05,
            max_depth=4, random_state=1,min_samples_leaf=3)
        clf2=sklearn.ensemble.GradientBoostingClassifier(n_estimators=100, learn_rate=.05,
            max_depth=4, random_state=1,min_samples_leaf=3)
    else:
        clf = sklearn.ensemble.GradientBoostingRegressor(n_estimators=100, learn_rate=.05,
            max_depth=4, random_state=1,min_samples_leaf=3)
        clf2=sklearn.ensemble.GradientBoostingRegressor(n_estimators=100, learn_rate=.05,
            max_depth=4, random_state=1,min_samples_leaf=3)
    return clf, clf2