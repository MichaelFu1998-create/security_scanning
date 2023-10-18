def _tryJson(data, raw=True):
    '''internal'''
    if raw:
        return data
    try:
        return json.loads(data)
    except ValueError:
        return data