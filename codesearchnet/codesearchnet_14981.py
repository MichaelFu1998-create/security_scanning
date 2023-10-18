def owsproxy_delegate(request):
    """
    Delegates owsproxy request to external twitcher service.
    """
    twitcher_url = request.registry.settings.get('twitcher.url')
    protected_path = request.registry.settings.get('twitcher.ows_proxy_protected_path', '/ows')
    url = twitcher_url + protected_path + '/proxy'
    if request.matchdict.get('service_name'):
        url += '/' + request.matchdict.get('service_name')
        if request.matchdict.get('access_token'):
            url += '/' + request.matchdict.get('service_name')
    url += '?' + urlparse.urlencode(request.params)
    LOGGER.debug("delegate to owsproxy: %s", url)
    # forward request to target (without Host Header)
    # h = dict(request.headers)
    # h.pop("Host", h)
    resp = requests.request(method=request.method.upper(), url=url, data=request.body,
                            headers=request.headers, verify=False)
    return Response(resp.content, status=resp.status_code, headers=resp.headers)