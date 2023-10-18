def to_yaml(model, sort=False, **kwargs):
    """
    Return the model as a YAML document.

    ``kwargs`` are passed on to ``yaml.dump``.

    Parameters
    ----------
    model : cobra.Model
        The cobra model to represent.
    sort : bool, optional
        Whether to sort the metabolites, reactions, and genes or maintain the
        order defined in the model.

    Returns
    -------
    str
        String representation of the cobra model as a YAML document.

    See Also
    --------
    save_yaml_model : Write directly to a file.
    ruamel.yaml.dump : Base function.
    """

    obj = model_to_dict(model, sort=sort)
    obj["version"] = YAML_SPEC
    return yaml.dump(obj, **kwargs)