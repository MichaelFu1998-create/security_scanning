def authenticate(self, request):
        """
        Returns two-tuple of (user, token) if authentication succeeds,
        or None otherwise.
        """
        try:
            oauth_request = oauth_provider.utils.get_oauth_request(request)
        except oauth.Error as err:
            raise exceptions.AuthenticationFailed(err.message)

        if not oauth_request:
            return None

        oauth_params = oauth_provider.consts.OAUTH_PARAMETERS_NAMES

        found = any(param for param in oauth_params if param in oauth_request)
        missing = list(param for param in oauth_params if param not in oauth_request)

        if not found:
            # OAuth authentication was not attempted.
            return None

        if missing:
            # OAuth was attempted but missing parameters.
            msg = 'Missing parameters: %s' % (', '.join(missing))
            raise exceptions.AuthenticationFailed(msg)

        if not self.check_nonce(request, oauth_request):
            msg = 'Nonce check failed'
            raise exceptions.AuthenticationFailed(msg)

        try:
            consumer_key = oauth_request.get_parameter('oauth_consumer_key')
            consumer = oauth_provider_store.get_consumer(request, oauth_request, consumer_key)
        except oauth_provider.store.InvalidConsumerError:
            msg = 'Invalid consumer token: %s' % oauth_request.get_parameter('oauth_consumer_key')
            raise exceptions.AuthenticationFailed(msg)

        if consumer.status != oauth_provider.consts.ACCEPTED:
            msg = 'Invalid consumer key status: %s' % consumer.get_status_display()
            raise exceptions.AuthenticationFailed(msg)

        try:
            token_param = oauth_request.get_parameter('oauth_token')
            token = oauth_provider_store.get_access_token(request, oauth_request, consumer, token_param)
        except oauth_provider.store.InvalidTokenError:
            msg = 'Invalid access token: %s' % oauth_request.get_parameter('oauth_token')
            raise exceptions.AuthenticationFailed(msg)

        try:
            self.validate_token(request, consumer, token)
        except oauth.Error as err:
            raise exceptions.AuthenticationFailed(err.message)

        user = token.user

        if not user.is_active:
            msg = 'User inactive or deleted: %s' % user.username
            raise exceptions.AuthenticationFailed(msg)

        return (token.user, token)