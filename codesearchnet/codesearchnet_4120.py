def create_model_path(model_path):
    """
    Creates a path to model files
    model_path - string
    """
    if not model_path.startswith("/") and not model_path.startswith("models/"):
        model_path="/" + model_path
    if not model_path.startswith("models"):
        model_path = "models" + model_path
    if not model_path.endswith(".p"):
        model_path+=".p"

    return model_path