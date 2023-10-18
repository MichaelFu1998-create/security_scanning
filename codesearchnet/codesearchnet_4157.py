def extract_features_and_generate_model(essays, algorithm=util_functions.AlgorithmTypes.regression):
    """
    Feed in an essay set to get feature vector and classifier
    essays must be an essay set object
    additional array is an optional argument that can specify
    a numpy array of values to add in
    returns a trained FeatureExtractor object and a trained classifier
    """
    f = feature_extractor.FeatureExtractor()
    f.initialize_dictionaries(essays)

    train_feats = f.gen_feats(essays)

    set_score = numpy.asarray(essays._score, dtype=numpy.int)
    if len(util_functions.f7(list(set_score)))>5:
        algorithm = util_functions.AlgorithmTypes.regression
    else:
        algorithm = util_functions.AlgorithmTypes.classification

    clf,clf2 = get_algorithms(algorithm)

    cv_error_results=get_cv_error(clf2,train_feats,essays._score)

    try:
        clf.fit(train_feats, set_score)
    except ValueError:
        log.exception("Not enough classes (0,1,etc) in sample.")
        set_score[0]=1
        set_score[1]=0
        clf.fit(train_feats, set_score)

    return f, clf, cv_error_results