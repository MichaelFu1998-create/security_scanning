def save_json_model(model, filename, sort=False, pretty=False, **kwargs):
    """
    Write the cobra model to a file in JSON format.

    ``kwargs`` are passed on to ``json.dump``.

    Parameters
    ----------
    model : cobra.Model
        The cobra model to represent.
    filename : str or file-like
        File path or descriptor that the JSON representation should be
        written to.
    sort : bool, optional
        Whether to sort the metabolites, reactions, and genes or maintain the
        order defined in the model.
    pretty : bool, optional
        Whether to format the JSON more compactly (default) or in a more
        verbose but easier to read fashion. Can be partially overwritten by the
        ``kwargs``.

    See Also
    --------
    to_json : Return a string representation.
    json.dump : Base function.
    """
    obj = model_to_dict(model, sort=sort)
    obj[u"version"] = JSON_SPEC

    if pretty:
        dump_opts = {
            "indent": 4, "separators": (",", ": "), "sort_keys": True,
            "allow_nan": False}
    else:
        dump_opts = {
            "indent": 0, "separators": (",", ":"), "sort_keys": False,
            "allow_nan": False}
    dump_opts.update(**kwargs)

    if isinstance(filename, string_types):
        with open(filename, "w") as file_handle:
            json.dump(obj, file_handle, **dump_opts)
    else:
        json.dump(obj, filename, **dump_opts)