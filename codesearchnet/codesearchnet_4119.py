def get_confidence_value(algorithm,model,grader_feats,score, scores):
    """
    Determines a confidence in a certain score, given proper input parameters
    algorithm- from util_functions.AlgorithmTypes
    model - a trained model
    grader_feats - a row of features used by the model for classification/regression
    score - The score assigned to the submission by a prior model
    """
    min_score=min(numpy.asarray(scores))
    max_score=max(numpy.asarray(scores))
    if algorithm == util_functions.AlgorithmTypes.classification and hasattr(model, "predict_proba"):
        #If classification, predict with probability, which gives you a matrix of confidences per score point
        raw_confidence=model.predict_proba(grader_feats)[0,(float(score)-float(min_score))]
        #TODO: Normalize confidence somehow here
        confidence=raw_confidence
    elif hasattr(model, "predict"):
        raw_confidence = model.predict(grader_feats)[0]
        confidence = max(float(raw_confidence) - math.floor(float(raw_confidence)), math.ceil(float(raw_confidence)) - float(raw_confidence))
    else:
        confidence = 0

    return confidence