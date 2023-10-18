def compose_err_msg(msg, **kwargs):
    """Append key-value pairs to msg, for display.

    Parameters
    ----------
    msg: string
        arbitrary message
    kwargs: dict
        arbitrary dictionary

    Returns
    -------
    updated_msg: string
        msg, with "key: value" appended. Only string values are appended.

    Example
    -------
    >>> compose_err_msg('Error message with arguments...', arg_num=123, \
        arg_str='filename.nii', arg_bool=True)
    'Error message with arguments...\\narg_str: filename.nii'
    >>>
    """
    updated_msg = msg
    for k, v in sorted(kwargs.items()):
        if isinstance(v, _basestring):  # print only str-like arguments
            updated_msg += "\n" + k + ": " + v

    return updated_msg