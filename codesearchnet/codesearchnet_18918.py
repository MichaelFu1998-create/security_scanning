def _hashkey(self, method, url, **kwa):
    '''Find a hash value for the linear combination of invocation methods.
    '''
    to_hash = ''.join([str(method), str(url),
        str(kwa.get('data', '')),
        str(kwa.get('params', ''))
    ])
    return hashlib.md5(to_hash.encode()).hexdigest()