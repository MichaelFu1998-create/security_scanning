def _raiseUnavailableFor401(message):
    ''' Returns a decorator to swallow a requests exception for modules that
        are not accessible without logging in, and turn it into an Unavailable
        exception.
    '''
    def __raiseUnavailableFor401(fn):
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == requests.codes.unauthorized:
                    raise access_common.Unavailable(message)
                else:
                    raise
        return wrapped
    return __raiseUnavailableFor401