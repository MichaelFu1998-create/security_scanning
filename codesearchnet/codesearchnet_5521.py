def _getJsonOrig(url):
    '''internal'''
    url = _URL_PREFIX + url
    resp = requests.get(urlparse(url).geturl(), proxies=_PYEX_PROXIES)
    if resp.status_code == 200:
        return resp.json()
    raise PyEXception('Response %d - ' % resp.status_code, resp.text)