def create_essay_set_and_dump_model(text,score,prompt,model_path,additional_array=None):
    """
    Function that creates essay set, extracts features, and writes out model
    See above functions for argument descriptions
    """
    essay_set=create_essay_set(text,score,prompt)
    feature_ext,clf=extract_features_and_generate_model(essay_set,additional_array)
    dump_model_to_file(prompt,feature_ext,clf,model_path)