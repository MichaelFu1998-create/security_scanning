def load_yaml_model(filename):
    """
    Load a cobra model from a file in YAML format.

    Parameters
    ----------
    filename : str or file-like
        File path or descriptor that contains the YAML document describing the
        cobra model.

    Returns
    -------
    cobra.Model
        The cobra model as represented in the YAML document.

    See Also
    --------
    from_yaml : Load from a string.
    """
    if isinstance(filename, string_types):
        with io.open(filename, "r") as file_handle:
            return model_from_dict(yaml.load(file_handle))
    else:
        return model_from_dict(yaml.load(filename))