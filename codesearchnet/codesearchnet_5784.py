def oauth_required(self, method):
        """Decorator that starts the OAuth 2.0 dance.

        Starts the OAuth dance for the logged in user if they haven't already
        granted access for this application.

        Args:
            method: callable, to be decorated method of a webapp.RequestHandler
                    instance.
        """

        def check_oauth(request_handler, *args, **kwargs):
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

            # Store the request URI in 'state' so we can use it later
            self.flow.params['state'] = _build_state_value(
                request_handler, user)
            self.credentials = self._storage_class(
                self._credentials_class, None,
                self._credentials_property_name, user=user).get()

            if not self.has_credentials():
                return request_handler.redirect(self.authorize_url())
            try:
                resp = method(request_handler, *args, **kwargs)
            except client.AccessTokenRefreshError:
                return request_handler.redirect(self.authorize_url())
            finally:
                self.credentials = None
            return resp

        return check_oauth