def _make_flow(self, return_url=None, **kwargs):
        """Creates a Web Server Flow"""
        # Generate a CSRF token to prevent malicious requests.
        csrf_token = hashlib.sha256(os.urandom(1024)).hexdigest()

        session[_CSRF_KEY] = csrf_token

        state = json.dumps({
            'csrf_token': csrf_token,
            'return_url': return_url
        })

        kw = self.flow_kwargs.copy()
        kw.update(kwargs)

        extra_scopes = kw.pop('scopes', [])
        scopes = set(self.scopes).union(set(extra_scopes))

        flow = client.OAuth2WebServerFlow(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=scopes,
            state=state,
            redirect_uri=url_for('oauth2.callback', _external=True),
            **kw)

        flow_key = _FLOW_KEY.format(csrf_token)
        session[flow_key] = pickle.dumps(flow)

        return flow