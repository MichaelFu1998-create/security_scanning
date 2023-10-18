def _stream(url, sendinit=None, on_data=print):
    '''internal'''
    cl = WSClient(url, sendinit=sendinit, on_data=on_data)
    return cl