def prepare_kwargs(raw, string_parameter='name'):
    """
    Utility method to convert raw string/diction input into a dictionary to pass
    into a function.  Always returns a dictionary.

    Args:
        raw: string or dictionary, string is assumed to be the name of the activation
                activation function.  Dictionary will be passed through unchanged.

    Returns: kwargs dictionary for **kwargs

    """
    kwargs = dict()

    if isinstance(raw, dict):
        kwargs.update(raw)
    elif isinstance(raw, str):
        kwargs[string_parameter] = raw

    return kwargs