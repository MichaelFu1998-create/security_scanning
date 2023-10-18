def dump_model_to_file(prompt_string, feature_ext, classifier, text, score, model_path):
    """
    Writes out a model to a file.
    prompt string is a string containing the prompt
    feature_ext is a trained FeatureExtractor object
    classifier is a trained classifier
    model_path is the path of write out the model file to
    """
    model_file = {'prompt': prompt_string, 'extractor': feature_ext, 'model': classifier, 'text' : text, 'score' : score}
    pickle.dump(model_file, file=open(model_path, "w"))