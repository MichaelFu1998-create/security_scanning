def evaluate_vars(data, context=None):
    """
    Evaluates variables in ``data``

    :param data: data structure containing variables, may be
                 ``str``, ``dict`` or ``list``
    :param context: ``dict`` containing variables
    :returns: modified data structure
    """
    context = context or {}
    if isinstance(data, (dict, list)):
        if isinstance(data, dict):
            loop_items = data.items()
        elif isinstance(data, list):
            loop_items = enumerate(data)
        for key, value in loop_items:
            data[key] = evaluate_vars(value, context)
    elif isinstance(data, six.string_types):
        vars_found = var_pattern.findall(data)
        for var in vars_found:
            var = var.strip()
            # if found multiple variables, create a new regexp pattern for each
            # variable, otherwise different variables would get the same value
            # (see https://github.com/openwisp/netjsonconfig/issues/55)
            if len(vars_found) > 1:
                pattern = r'\{\{(\s*%s\s*)\}\}' % var
            # in case of single variables, use the precompiled
            # regexp pattern to save computation
            else:
                pattern = var_pattern
            if var in context:
                data = re.sub(pattern, context[var], data)
    return data