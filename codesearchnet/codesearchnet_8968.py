def _list_errors(e):
    """
    Returns a list of violated schema fragments and related error messages
    :param e: ``jsonschema.exceptions.ValidationError`` instance
    """
    error_list = []
    for value, error in zip(e.validator_value, e.context):
        error_list.append((value, error.message))
        if error.context:
            error_list += _list_errors(error)
    return error_list