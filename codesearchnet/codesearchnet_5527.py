def _streamSSE(url, on_data=print, accrue=False):
    '''internal'''
    messages = SSEClient(url)
    if accrue:
        ret = []

    for msg in messages:
        data = msg.data
        on_data(json.loads(data))
        if accrue:
            ret.append(msg)

    return ret