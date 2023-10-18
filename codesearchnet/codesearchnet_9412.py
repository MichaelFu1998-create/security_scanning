def jsonify_status_code(status_code, *args, **kw):
    """Returns a jsonified response with the specified HTTP status code.

    The positional and keyword arguments are passed directly to the
    :func:`flask.jsonify` function which creates the response.
    """
    is_batch = kw.pop('is_batch', False)
    if is_batch:
        response = flask_make_response(json.dumps(*args, **kw))
        response.mimetype = 'application/json'
        response.status_code = status_code
        return response
    response = jsonify(*args, **kw)
    response.status_code = status_code
    return response