def search(query='', keywords=[], registry=None):
    ''' generator of objects returned by the search endpoint (both modules and
        targets).

        Query is a full-text search (description, name, keywords), keywords
        search only the module/target description keywords lists.

        If both parameters are specified the search is the intersection of the
        two queries.
    '''
    registry = registry or Registry_Base_URL

    url = '%s/search' % registry

    headers = _headersForRegistry(registry)

    params = {
         'skip': 0,
        'limit': 50
    }
    if len(query):
        params['query'] = query
    if len(keywords):
        params['keywords[]'] = keywords

    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        objects = ordered_json.loads(response.text)
        if len(objects):
            for o in objects:
                yield o
            params['skip'] += params['limit']
        else:
            break