def _pybossa_req(method, domain, id=None, payload=None, params={},
                 headers={'content-type': 'application/json'},
                 files=None):
    """
    Send a JSON request.

    Returns True if everything went well, otherwise it returns the status
    code of the response.
    """
    url = _opts['endpoint'] + '/api/' + domain
    if id is not None:
        url += '/' + str(id)
    if 'api_key' in _opts:
        params['api_key'] = _opts['api_key']
    if method == 'get':
        r = requests.get(url, params=params)
    elif method == 'post':
        if files is None and headers['content-type'] == 'application/json':
            r = requests.post(url, params=params, headers=headers,
                              data=json.dumps(payload))
        else:
            r = requests.post(url, params=params, files=files, data=payload)
    elif method == 'put':
        r = requests.put(url, params=params, headers=headers,
                         data=json.dumps(payload))
    elif method == 'delete':
        r = requests.delete(url, params=params, headers=headers,
                            data=json.dumps(payload))
    if r.status_code // 100 == 2:
        if r.text and r.text != '""':
            return json.loads(r.text)
        else:
            return True
    else:
        return json.loads(r.text)