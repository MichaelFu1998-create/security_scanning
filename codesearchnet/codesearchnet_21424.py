def request(key, features, query, timeout=5):
    """Make an API request

    :param string key: API key to use
    :param list features: features to request. It must be a subset of :data:`FEATURES`
    :param string query: query to send
    :param integer timeout: timeout of the request
    :returns: result of the API request
    :rtype: dict

    """
    data = {}
    data['key'] = key
    data['features'] = '/'.join([f for f in features if f in FEATURES])
    data['query'] = quote(query)
    data['format'] = 'json'
    r = requests.get(API_URL.format(**data), timeout=timeout)
    results = json.loads(_unicode(r.content))
    return results