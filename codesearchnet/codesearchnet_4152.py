def create_generic(numeric_values, textual_values, target, algorithm = util_functions.AlgorithmTypes.regression):
    """
    Creates a model from a generic list numeric values and text values
    numeric_values - A list of lists that are the predictors
    textual_values - A list of lists that are the predictors
    (each item in textual_values corresponds to the similarly indexed counterpart in numeric_values)
    target - The variable that we are trying to predict.  A list of integers.
    algorithm - the type of algorithm that will be used
    """

    algorithm = select_algorithm(target)
    #Initialize a result dictionary to return.
    results = {'errors': [],'success' : False, 'cv_kappa' : 0, 'cv_mean_absolute_error': 0,
               'feature_ext' : "", 'classifier' : "", 'algorithm' : algorithm}

    if len(numeric_values)!=len(textual_values) or len(numeric_values)!=len(target):
        msg = "Target, numeric features, and text features must all be the same length."
        results['errors'].append(msg)
        log.exception(msg)
        return results

    try:
        #Initialize a predictor set object that encapsulates all of the text and numeric predictors
        pset = predictor_set.PredictorSet(essaytype="train")
        for i in xrange(0, len(numeric_values)):
            pset.add_row(numeric_values[i], textual_values[i], target[i])
    except:
        msg = "predictor set creation failed."
        results['errors'].append(msg)
        log.exception(msg)

    try:
        #Extract all features and then train a classifier with the features
        feature_ext, classifier, cv_error_results = model_creator.extract_features_and_generate_model_predictors(pset, algorithm)
        results['cv_kappa']=cv_error_results['kappa']
        results['cv_mean_absolute_error']=cv_error_results['mae']
        results['feature_ext']=feature_ext
        results['classifier']=classifier
        results['success']=True
    except:
        msg = "feature extraction and model creation failed."
        results['errors'].append(msg)
        log.exception(msg)

    return results