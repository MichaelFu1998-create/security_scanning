def callback_view(self):
        """Flask view that handles the user's return from OAuth2 provider.

        On return, exchanges the authorization code for credentials and stores
        the credentials.
        """
        if 'error' in request.args:
            reason = request.args.get(
                'error_description', request.args.get('error', ''))
            reason = markupsafe.escape(reason)
            return ('Authorization failed: {0}'.format(reason),
                    httplib.BAD_REQUEST)

        try:
            encoded_state = request.args['state']
            server_csrf = session[_CSRF_KEY]
            code = request.args['code']
        except KeyError:
            return 'Invalid request', httplib.BAD_REQUEST

        try:
            state = json.loads(encoded_state)
            client_csrf = state['csrf_token']
            return_url = state['return_url']
        except (ValueError, KeyError):
            return 'Invalid request state', httplib.BAD_REQUEST

        if client_csrf != server_csrf:
            return 'Invalid request state', httplib.BAD_REQUEST

        flow = _get_flow_for_token(server_csrf)

        if flow is None:
            return 'Invalid request state', httplib.BAD_REQUEST

        # Exchange the auth code for credentials.
        try:
            credentials = flow.step2_exchange(code)
        except client.FlowExchangeError as exchange_error:
            current_app.logger.exception(exchange_error)
            content = 'An error occurred: {0}'.format(exchange_error)
            return content, httplib.BAD_REQUEST

        # Save the credentials to the storage.
        self.storage.put(credentials)

        if self.authorize_callback:
            self.authorize_callback(credentials)

        return redirect(return_url)