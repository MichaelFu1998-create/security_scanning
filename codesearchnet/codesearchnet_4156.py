def extract_features_and_generate_model_predictors(predictor_set, algorithm=util_functions.AlgorithmTypes.regression):
    """
    Extracts features and generates predictors based on a given predictor set
    predictor_set - a PredictorSet object that has been initialized with data
    type - one of util_functions.AlgorithmType
    """
    if(algorithm not in [util_functions.AlgorithmTypes.regression, util_functions.AlgorithmTypes.classification]):
        algorithm = util_functions.AlgorithmTypes.regression

    f = predictor_extractor.PredictorExtractor()
    f.initialize_dictionaries(predictor_set)

    train_feats = f.gen_feats(predictor_set)

    clf,clf2 = get_algorithms(algorithm)
    cv_error_results=get_cv_error(clf2,train_feats,predictor_set._target)

    try:
        set_score = numpy.asarray(predictor_set._target, dtype=numpy.int)
        clf.fit(train_feats, set_score)
    except ValueError:
        log.exception("Not enough classes (0,1,etc) in sample.")
        set_score = predictor_set._target
        set_score[0]=1
        set_score[1]=0
        clf.fit(train_feats, set_score)

    return f, clf, cv_error_results