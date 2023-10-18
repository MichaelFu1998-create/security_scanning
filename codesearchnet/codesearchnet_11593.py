def _returnRequestError(fn):
    ''' Decorator that captures requests.exceptions.RequestException errors
        and returns them as an error message. If no error occurs the reture
        value of the wrapped function is returned (normally None). '''
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            return "server returned status %s: %s" % (e.response.status_code, e.message)
    return wrapped