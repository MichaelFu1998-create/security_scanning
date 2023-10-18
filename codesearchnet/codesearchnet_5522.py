def _getJsonIEXCloud(url, token='', version='beta'):
    '''for iex cloud'''
    url = _URL_PREFIX2.format(version=version) + url
    resp = requests.get(urlparse(url).geturl(), proxies=_PYEX_PROXIES, params={'token': token})
    if resp.status_code == 200:
        return resp.json()
    raise PyEXception('Response %d - ' % resp.status_code, resp.text)