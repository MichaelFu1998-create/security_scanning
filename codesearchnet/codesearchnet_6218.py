def save_yaml_model(model, filename, sort=False, **kwargs):
    """
    Write the cobra model to a file in YAML format.

    ``kwargs`` are passed on to ``yaml.dump``.

    Parameters
    ----------
    model : cobra.Model
        The cobra model to represent.
    filename : str or file-like
        File path or descriptor that the YAML representation should be
        written to.
    sort : bool, optional
        Whether to sort the metabolites, reactions, and genes or maintain the
        order defined in the model.

    See Also
    --------
    to_yaml : Return a string representation.
    ruamel.yaml.dump : Base function.
    """
    obj = model_to_dict(model, sort=sort)
    obj["version"] = YAML_SPEC
    if isinstance(filename, string_types):
        with io.open(filename, "w") as file_handle:
            yaml.dump(obj, file_handle, **kwargs)
    else:
        yaml.dump(obj, filename, **kwargs)