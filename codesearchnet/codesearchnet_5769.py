def required(self, decorated_function=None, scopes=None,
                 **decorator_kwargs):
        """Decorator to require OAuth2 credentials for a view.

        If credentials are not available for the current user, then they will
        be redirected to the authorization flow. Once complete, the user will
        be redirected back to the original page.
        """

        def curry_wrapper(wrapped_function):
            @wraps(wrapped_function)
            def required_wrapper(*args, **kwargs):
                return_url = decorator_kwargs.pop('return_url', request.url)

                requested_scopes = set(self.scopes)
                if scopes is not None:
                    requested_scopes |= set(scopes)
                if self.has_credentials():
                    requested_scopes |= self.credentials.scopes

                requested_scopes = list(requested_scopes)

                # Does the user have credentials and does the credentials have
                # all of the needed scopes?
                if (self.has_credentials() and
                        self.credentials.has_scopes(requested_scopes)):
                    return wrapped_function(*args, **kwargs)
                # Otherwise, redirect to authorization
                else:
                    auth_url = self.authorize_url(
                        return_url,
                        scopes=requested_scopes,
                        **decorator_kwargs)

                    return redirect(auth_url)

            return required_wrapper

        if decorated_function:
            return curry_wrapper(decorated_function)
        else:
            return curry_wrapper