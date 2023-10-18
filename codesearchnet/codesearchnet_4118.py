def grade_generic(grader_data, numeric_features, textual_features):
    """
    Grades a set of numeric and textual features using a generic model
    grader_data -- dictionary containing:
    {
        'algorithm' - Type of algorithm to use to score
    }
    numeric_features - list of numeric features to predict on
    textual_features - list of textual feature to predict on

    """
    results = {'errors': [],'tests': [],'score': 0, 'success' : False, 'confidence' : 0}

    has_error=False

    #Try to find and load the model file

    grader_set=predictor_set.PredictorSet(essaytype="test")

    model, extractor = get_classifier_and_ext(grader_data)

    #Try to add essays to essay set object
    try:
        grader_set.add_row(numeric_features, textual_features,0)
    except Exception:
        error_msg = "Row could not be added to predictor set:{0} {1}".format(numeric_features, textual_features)
        log.exception(error_msg)
        results['errors'].append(error_msg)
        has_error=True

    #Try to extract features from submission and assign score via the model
    try:
        grader_feats=extractor.gen_feats(grader_set)
        results['score']=model.predict(grader_feats)[0]
    except Exception:
        error_msg = "Could not extract features and score essay."
        log.exception(error_msg)
        results['errors'].append(error_msg)
        has_error=True

    #Try to determine confidence level
    try:
        results['confidence'] = get_confidence_value(grader_data['algorithm'],model, grader_feats, results['score'])
    except Exception:
        #If there is an error getting confidence, it is not a show-stopper, so just log
        log.exception("Problem generating confidence value")

    if not has_error:
        results['success'] = True

    return results