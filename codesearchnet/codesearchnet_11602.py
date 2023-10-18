def setAPIKey(registry, api_key):
    ''' Set the api key for accessing a registry. This is only necessary for
        development/test registries.
    '''
    if (registry is None) or (registry == Registry_Base_URL):
        return
    sources = _getSources()
    source = None
    for s in sources:
        if _sourceMatches(s, registry):
            source = s
    if source is None:
        source = {
           'type':'registry',
            'url':registry,
        }
        sources.append(source)
    source['apikey'] = api_key
    settings.set('sources', sources)