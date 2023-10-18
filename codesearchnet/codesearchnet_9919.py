def __entry_point():
    """
        Function called when an query is made on /json. Expects a JSON
        object with at least a 'method' entry.
    """
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Empty User-Agent')
    method = request.json.get('method')
    if method is None:
        __query_logging(ip, ua, method, level='warning')
        return json.dumps({'error': 'No method provided.'})
    if method not in authorized_methods:
        # unauthorized query
        __query_logging(ip, ua, method, level='warning')
        return json.dumps({'error': 'Unauthorized method.'})
    fct = globals().get(method)
    if fct is None:
        # unknown method, the method is authorized, but does not exists...
        __query_logging(ip, ua, method, level='warning')
        return json.dumps({'error': 'Unknown method.'})
    if request.json.get('ip') is None:
        __query_logging(ip, ua, method, level='warning')
        return json.dumps({'error': 'No IP provided, not going to work.'})
    try:
        result = fct(request.json)
        __query_logging(ip, ua, method, request.json.get('ip'),
                        request.json.get('announce_date'), request.json.get('days_limit'))
        return result
    except Exception:
        __query_logging(ip, ua, method, request.json.get('ip'), level='error')
        return json.dumps({'error': 'Something went wrong.'})