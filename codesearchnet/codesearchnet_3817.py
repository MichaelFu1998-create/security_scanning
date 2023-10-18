def fetch_token(
        self,
        token_url,
        code=None,
        authorization_response=None,
        body="",
        auth=None,
        username=None,
        password=None,
        method="POST",
        force_querystring=False,
        timeout=None,
        headers=None,
        verify=True,
        proxies=None,
        include_client_id=None,
        client_secret=None,
        **kwargs
    ):
        """Generic method for fetching an access token from the token endpoint.

        If you are using the MobileApplicationClient you will want to use
        `token_from_fragment` instead of `fetch_token`.

        The current implementation enforces the RFC guidelines.

        :param token_url: Token endpoint URL, must use HTTPS.
        :param code: Authorization code (used by WebApplicationClients).
        :param authorization_response: Authorization response URL, the callback
                                       URL of the request back to you. Used by
                                       WebApplicationClients instead of code.
        :param body: Optional application/x-www-form-urlencoded body to add the
                     include in the token request. Prefer kwargs over body.
        :param auth: An auth tuple or method as accepted by `requests`.
        :param username: Username required by LegacyApplicationClients to appear
                         in the request body.
        :param password: Password required by LegacyApplicationClients to appear
                         in the request body.
        :param method: The HTTP method used to make the request. Defaults
                       to POST, but may also be GET. Other methods should
                       be added as needed.
        :param force_querystring: If True, force the request body to be sent
            in the querystring instead.
        :param timeout: Timeout of the request in seconds.
        :param headers: Dict to default request headers with.
        :param verify: Verify SSL certificate.
        :param proxies: The `proxies` argument is passed onto `requests`.
        :param include_client_id: Should the request body include the
                                  `client_id` parameter. Default is `None`,
                                  which will attempt to autodetect. This can be
                                  forced to always include (True) or never
                                  include (False).
        :param client_secret: The `client_secret` paired to the `client_id`.
                              This is generally required unless provided in the
                              `auth` tuple. If the value is `None`, it will be
                              omitted from the request, however if the value is
                              an empty string, an empty string will be sent.
        :param kwargs: Extra parameters to include in the token request.
        :return: A token dict
        """
        if not is_secure_transport(token_url):
            raise InsecureTransportError()

        if not code and authorization_response:
            self._client.parse_request_uri_response(
                authorization_response, state=self._state
            )
            code = self._client.code
        elif not code and isinstance(self._client, WebApplicationClient):
            code = self._client.code
            if not code:
                raise ValueError(
                    "Please supply either code or " "authorization_response parameters."
                )

        # Earlier versions of this library build an HTTPBasicAuth header out of
        # `username` and `password`. The RFC states, however these attributes
        # must be in the request body and not the header.
        # If an upstream server is not spec compliant and requires them to
        # appear as an Authorization header, supply an explicit `auth` header
        # to this function.
        # This check will allow for empty strings, but not `None`.
        #
        # Refernences
        # 4.3.2 - Resource Owner Password Credentials Grant
        #         https://tools.ietf.org/html/rfc6749#section-4.3.2

        if isinstance(self._client, LegacyApplicationClient):
            if username is None:
                raise ValueError(
                    "`LegacyApplicationClient` requires both the "
                    "`username` and `password` parameters."
                )
            if password is None:
                raise ValueError(
                    "The required paramter `username` was supplied, "
                    "but `password` was not."
                )

        # merge username and password into kwargs for `prepare_request_body`
        if username is not None:
            kwargs["username"] = username
        if password is not None:
            kwargs["password"] = password

        # is an auth explicitly supplied?
        if auth is not None:
            # if we're dealing with the default of `include_client_id` (None):
            # we will assume the `auth` argument is for an RFC compliant server
            # and we should not send the `client_id` in the body.
            # This approach allows us to still force the client_id by submitting
            # `include_client_id=True` along with an `auth` object.
            if include_client_id is None:
                include_client_id = False

        # otherwise we may need to create an auth header
        else:
            # since we don't have an auth header, we MAY need to create one
            # it is possible that we want to send the `client_id` in the body
            # if so, `include_client_id` should be set to True
            # otherwise, we will generate an auth header
            if include_client_id is not True:
                client_id = self.client_id
                if client_id:
                    log.debug(
                        'Encoding `client_id` "%s" with `client_secret` '
                        "as Basic auth credentials.",
                        client_id,
                    )
                    client_secret = client_secret if client_secret is not None else ""
                    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

        if include_client_id:
            # this was pulled out of the params
            # it needs to be passed into prepare_request_body
            if client_secret is not None:
                kwargs["client_secret"] = client_secret

        body = self._client.prepare_request_body(
            code=code,
            body=body,
            redirect_uri=self.redirect_uri,
            include_client_id=include_client_id,
            **kwargs
        )

        headers = headers or {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        self.token = {}
        request_kwargs = {}
        if method.upper() == "POST":
            request_kwargs["params" if force_querystring else "data"] = dict(
                urldecode(body)
            )
        elif method.upper() == "GET":
            request_kwargs["params"] = dict(urldecode(body))
        else:
            raise ValueError("The method kwarg must be POST or GET.")

        r = self.request(
            method=method,
            url=token_url,
            timeout=timeout,
            headers=headers,
            auth=auth,
            verify=verify,
            proxies=proxies,
            **request_kwargs
        )

        log.debug("Request to fetch token completed with status %s.", r.status_code)
        log.debug("Request url was %s", r.request.url)
        log.debug("Request headers were %s", r.request.headers)
        log.debug("Request body was %s", r.request.body)
        log.debug("Response headers were %s and content %s.", r.headers, r.text)
        log.debug(
            "Invoking %d token response hooks.",
            len(self.compliance_hook["access_token_response"]),
        )
        for hook in self.compliance_hook["access_token_response"]:
            log.debug("Invoking hook %s.", hook)
            r = hook(r)

        self._client.parse_request_body_response(r.text, scope=self.scope)
        self.token = self._client.token
        log.debug("Obtained token %s.", self.token)
        return self.token