def oauth_aware(self, method):
        """Decorator that sets up for OAuth 2.0 dance, but doesn't do it.

        Does all the setup for the OAuth dance, but doesn't initiate it.
        This decorator is useful if you want to create a page that knows
        whether or not the user has granted access to this application.
        From within a method decorated with @oauth_aware the has_credentials()
        and authorize_url() methods can be called.

        Args:
            method: callable, to be decorated method of a webapp.RequestHandler
                    instance.
        """

        def setup_oauth(request_handler, *args, **kwargs):
            if self._in_error:
                self._display_error_message(request_handler)
                return

            user = users.get_current_user()
            # Don't use @login_decorator as this could be used in a
            # POST request.
            if not user:
                request_handler.redirect(users.create_login_url(
                    request_handler.request.uri))
                return

            self._create_flow(request_handler)

            self.flow.params['state'] = _build_state_value(request_handler,
                                                           user)
            self.credentials = self._storage_class(
                self._credentials_class, None,
                self._credentials_property_name, user=user).get()
            try:
                resp = method(request_handler, *args, **kwargs)
            finally:
                self.credentials = None
            return resp
        return setup_oauth