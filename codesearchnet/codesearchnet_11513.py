def instance_from_str(instance_str):
    """
    Given an instance string in the form "app.Model:pk", returns a tuple of
    ``(model, instance)``. If the pk part is empty, ``instance`` will be
    ``None``. Raises ``ValueError`` on invalid model strings or missing
    instances.
    """
    match = instance_str_re.match(instance_str)
    if not match:
        raise ValueError("Invalid instance string")

    model_string = match.group(1)
    try:
        model = apps.get_model(model_string)
    except (LookupError, ValueError):
        raise ValueError("Invalid instance string")

    pk = match.group(2)
    if pk:
        try:
            return model, model._default_manager.get(pk=pk)
        except model.DoesNotExist:
            raise ValueError("Invalid instance string")

    return model, None