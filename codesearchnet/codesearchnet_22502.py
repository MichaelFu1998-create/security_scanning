def get_param_values(request, model=None):
    """
    Converts the request parameters to Python.

    :param request: <pyramid.request.Request> || <dict>

    :return: <dict>
    """
    if type(request) == dict:
        return request

    params = get_payload(request)

    # support in-place editing formatted request
    try:
        del params['pk']
        params[params.pop('name')] = params.pop('value')
    except KeyError:
        pass

    return {
        k.rstrip('[]'): safe_eval(v) if not type(v) == list else [safe_eval(sv) for sv in v]
        for k, v in params.items()
    }