def get_context(request, model=None):
    """
    Extracts ORB context information from the request.

    :param request: <pyramid.request.Request>
    :param model: <orb.Model> || None

    :return: {<str> key: <variant> value} values, <orb.Context>
    """
    # convert request parameters to python
    param_values = get_param_values(request, model=model)

    # extract the full orb context if provided
    context = param_values.pop('orb_context', {})
    if isinstance(context, (unicode, str)):
        context = projex.rest.unjsonify(context)

    # otherwise, extract the limit information
    has_limit = 'limit' in context or 'limit' in param_values

    # create the new orb context
    orb_context = orb.Context(**context)

    # build up context information from the request params
    used = set()
    query_context = {}
    for key in orb.Context.Defaults:
        if key in param_values:
            used.add(key)
            query_context[key] = param_values.get(key)

    # generate a simple query object
    schema_values = {}
    if model:
        # extract match dict items
        for key, value in request.matchdict.items():
            if model.schema().column(key, raise_=False):
                schema_values[key] = value

        # extract payload items
        for key, value in param_values.items():
            root_key = key.split('.')[0]
            schema_object = model.schema().column(root_key, raise_=False) or model.schema().collector(root_key)
            if schema_object:
                value = param_values.pop(key)
                if isinstance(schema_object, orb.Collector) and type(value) not in (tuple, list):
                    value = [value]
                schema_values[key] = value

    # generate the base context information
    query_context['scope'] = {
        'request': request
    }

    # include any request specific scoping or information from the request
    # first, look for default ORB context for all requests
    try:
        default_context = request.orb_default_context

    # then, look for scope specific information for all requests
    except AttributeError:
        try:
            query_context['scope'].update(request.orb_scope)
        except AttributeError:
            pass

    # if request specific context defaults exist, then
    # merge them with the rest of the query context
    else:
        if 'scope' in default_context:
            query_context['scope'].update(default_context.pop('scope'))

        # setup defaults based on the request
        for k, v in default_context.items():
            query_context.setdefault(k, v)

    orb_context.update(query_context)
    return schema_values, orb_context