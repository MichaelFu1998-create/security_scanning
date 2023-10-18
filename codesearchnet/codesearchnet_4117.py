def grade(grader_data,submission):
    """
    Grades a specified submission using specified models
    grader_data - A dictionary:
    {
        'model' : trained model,
        'extractor' : trained feature extractor,
        'prompt' : prompt for the question,
        'algorithm' : algorithm for the question,
    }
    submission - The student submission (string)
    """

    #Initialize result dictionary
    results = {'errors': [],'tests': [],'score': 0, 'feedback' : "", 'success' : False, 'confidence' : 0}
    has_error=False

    grader_set=EssaySet(essaytype="test")
    feedback = {}

    model, extractor = get_classifier_and_ext(grader_data)

    #This is to preserve legacy functionality
    if 'algorithm' not in grader_data:
        grader_data['algorithm'] = util_functions.AlgorithmTypes.classification

    try:
        #Try to add essay to essay set object
        grader_set.add_essay(str(submission),0)
        grader_set.update_prompt(str(grader_data['prompt']))
    except Exception:
        error_message = "Essay could not be added to essay set:{0}".format(submission)
        log.exception(error_message)
        results['errors'].append(error_message)
        has_error=True

    #Try to extract features from submission and assign score via the model
    try:
        grader_feats=extractor.gen_feats(grader_set)
        feedback=extractor.gen_feedback(grader_set,grader_feats)[0]
        results['score']=int(model.predict(grader_feats)[0])
    except Exception:
        error_message = "Could not extract features and score essay."
        log.exception(error_message)
        results['errors'].append(error_message)
        has_error=True

    #Try to determine confidence level
    try:
        results['confidence'] = get_confidence_value(grader_data['algorithm'], model, grader_feats, results['score'], grader_data['score'])
    except Exception:
        #If there is an error getting confidence, it is not a show-stopper, so just log
        log.exception("Problem generating confidence value")

    if not has_error:

        #If the essay is just a copy of the prompt, return a 0 as the score
        if( 'too_similar_to_prompt' in feedback and feedback['too_similar_to_prompt']):
            results['score']=0
            results['correct']=False

        results['success']=True

        #Generate short form output--number of problem areas identified in feedback

        #Add feedback to results if available
        results['feedback'] = {}
        if 'topicality' in feedback and 'prompt_overlap' in feedback:
            results['feedback'].update({
                'topicality' : feedback['topicality'],
                'prompt-overlap' : feedback['prompt_overlap'],
                })

        results['feedback'].update(
            {
                'spelling' : feedback['spelling'],
                'grammar' : feedback['grammar'],
                'markup-text' : feedback['markup_text'],
                }
        )

    else:
        #If error, success is False.
        results['success']=False

    return results