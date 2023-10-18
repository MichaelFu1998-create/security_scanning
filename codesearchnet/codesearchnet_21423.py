def autocomplete(query, country=None, hurricanes=False, cities=True, timeout=5):
    """Make an autocomplete API request

    This can be used to find cities and/or hurricanes by name

    :param string query: city
    :param string country: restrict search to a specific country. Must be a two letter country code
    :param boolean hurricanes: whether to search for hurricanes or not
    :param boolean cities: whether to search for cities or not
    :param integer timeout: timeout of the api request
    :returns: result of the autocomplete API request
    :rtype: dict

    """
    data = {}
    data['query'] = quote(query)
    data['country'] = country or ''
    data['hurricanes'] = 1 if hurricanes else 0
    data['cities'] = 1 if cities else 0
    data['format'] = 'JSON'
    r = requests.get(AUTOCOMPLETE_URL.format(**data), timeout=timeout)
    results = json.loads(r.content)['RESULTS']
    return results