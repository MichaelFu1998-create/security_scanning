def _handleAuth(fn):
    ''' Decorator to re-try API calls after asking the user for authentication. '''
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        # auth, , authenticate users, internal
        from yotta.lib import auth
        # if yotta is being run noninteractively, then we never retry, but we
        # do call auth.authorizeUser, so that a login URL can be displayed:
        interactive = globalconf.get('interactive')
        try:
            return fn(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == requests.codes.unauthorized: #pylint: disable=no-member
                logger.debug('%s unauthorised', fn)
                # any provider is sufficient for registry auth
                auth.authorizeUser(provider=None, interactive=interactive)
                if interactive:
                    logger.debug('retrying after authentication...')
                    return fn(*args, **kwargs)
            raise
    return wrapped