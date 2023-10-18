def _replace(_self, **kwds):
        'Return a new SplitResult object replacing specified fields with new values'
        result = _self._make(map(kwds.pop, ('scheme', 'netloc', 'path', 'query', 'fragment'), _self))
        if kwds:
            raise ValueError('Got unexpected field names: %r' % kwds.keys())
        return result