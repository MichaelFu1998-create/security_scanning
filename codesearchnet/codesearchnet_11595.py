def _friendlyAuthError(fn):
    ''' Decorator to print a friendly you-are-not-authorised message. Use
        **outside** the _handleAuth decorator to only print the message after
        the user has been given a chance to login. '''
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == requests.codes.unauthorized: #pylint: disable=no-member
                logger.error('insufficient permission')
            elif e.response.status_code == requests.codes.bad and 'jwt has expired' in e.response.text.lower(): #pylint: disable=no-member
                logger.error('server returned status %s: %s', e.response.status_code, e.response.text)
                logger.error('Check that your system clock is set accurately!')
            else:
                logger.error('server returned status %s: %s', e.response.status_code, e.response.text)
            raise
    return wrapped