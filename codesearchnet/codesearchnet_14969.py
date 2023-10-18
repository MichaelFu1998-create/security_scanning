def authenticate_credentials(self, userargs, password, request=None):
        """
        Authenticate the userargs and password against Django auth backends.
        The "userargs" string may be just the username, or a querystring-encoded set of params.
        """

        credentials = {
            'password': password
        }

        if "=" not in userargs:
            # if it doesn't seem to be in querystring format, just use it as the username
            credentials[get_user_model().USERNAME_FIELD] = userargs
        else:
            # parse out the user args from querystring format into the credentials dict
            for arg in userargs.split("&"):
                key, val = arg.split("=")
                credentials[key] = val

        # authenticate the user via Django's auth backends
        user = authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (user, None)