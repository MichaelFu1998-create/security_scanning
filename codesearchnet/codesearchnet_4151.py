def create(text,score,prompt_string, dump_data=False):
    """
    Creates a machine learning model from input text, associated scores, a prompt, and a path to the model
    TODO: Remove model path argument, it is needed for now to support legacy code
    text - A list of strings containing the text of the essays
    score - a list of integers containing score values
    prompt_string - the common prompt for the set of essays
    """

    if dump_data:
        dump_input_data(text, score)

    algorithm = select_algorithm(score)
    #Initialize a results dictionary to return
    results = {'errors': [],'success' : False, 'cv_kappa' : 0, 'cv_mean_absolute_error': 0,
               'feature_ext' : "", 'classifier' : "", 'algorithm' : algorithm,
               'score' : score, 'text' : text, 'prompt' : prompt_string}

    if len(text)!=len(score):
        msg = "Target and text lists must be same length."
        results['errors'].append(msg)
        log.exception(msg)
        return results

    try:
        #Create an essay set object that encapsulates all the essays and alternate representations (tokens, etc)
        e_set = model_creator.create_essay_set(text, score, prompt_string)
    except:
        msg = "essay set creation failed."
        results['errors'].append(msg)
        log.exception(msg)
    try:
        #Gets features from the essay set and computes error
        feature_ext, classifier, cv_error_results = model_creator.extract_features_and_generate_model(e_set, algorithm = algorithm)
        results['cv_kappa']=cv_error_results['kappa']
        results['cv_mean_absolute_error']=cv_error_results['mae']
        results['feature_ext']=feature_ext
        results['classifier']=classifier
        results['algorithm'] = algorithm
        results['success']=True
    except:
        msg = "feature extraction and model creation failed."
        results['errors'].append(msg)
        log.exception(msg)

    return results