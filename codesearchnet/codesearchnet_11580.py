def _handleAuth(fn):
    ''' Decorator to re-try API calls after asking the user for authentication. '''
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        # if yotta is being run noninteractively, then we never retry, but we
        # do call auth.authorizeUser, so that a login URL can be displayed:
        interactive = globalconf.get('interactive')

        def retryWithAuthOrRaise(original_exception):
            # in all cases ask for auth, so that in non-interactive mode a
            # login URL is displayed
            auth.authorizeUser(provider='github', interactive=interactive)
            if not interactive:
                raise original_exception
            else:
                logger.debug('trying with authtoken: %s', settings.getProperty('github', 'authtoken'))
                return fn(*args, **kwargs)

        # authorised requests have a higher rate limit, but display a warning
        # message in this case, as the user might not expect the requirement to
        # auth:
        def handleRateLimitExceeded(original_exception):
            if not _userAuthedWithGithub():
                logger.warning('github rate limit for anonymous requests exceeded: you must log in')
                return retryWithAuthOrRaise(original_exception)
            else:
                raise original_exception

        try:
            return fn(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                # 403 = rate limit exceeded
                return handleRateLimitExceeded(e)
            if e.response.status_code == 401:
                # 401 = unauthorised
                return retryWithAuthOrRaise(e)
            raise
        except github.BadCredentialsException as e:
            logger.debug("github: bad credentials")
            return retryWithAuthOrRaise(e)
        except github.UnknownObjectException as e:
            logger.debug("github: unknown object")
            # some endpoints return 404 if the user doesn't have access, maybe
            # it would be better to prompt for another username and password,
            # and store multiple tokens that we can try for each request....
            # but for now we assume that if the user is logged in then a 404
            # really is a 404
            if not _userAuthedWithGithub():
                logger.info('failed to fetch Github object, re-trying with authentication...')
                return retryWithAuthOrRaise(e)
            raise
        except github.RateLimitExceededException as e:
            return handleRateLimitExceeded(e)
        except github.GithubException as e:
            if e.status == 403:
                # 403 = rate limit exceeded
                return handleRateLimitExceeded(e)
            raise
    return wrapped