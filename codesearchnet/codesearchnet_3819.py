def refresh_token(
        self,
        token_url,
        refresh_token=None,
        body="",
        auth=None,
        timeout=None,
        headers=None,
        verify=True,
        proxies=None,
        **kwargs
    ):
        """Fetch a new access token using a refresh token.

        :param token_url: The token endpoint, must be HTTPS.
        :param refresh_token: The refresh_token to use.
        :param body: Optional application/x-www-form-urlencoded body to add the
                     include in the token request. Prefer kwargs over body.
        :param auth: An auth tuple or method as accepted by `requests`.
        :param timeout: Timeout of the request in seconds.
        :param headers: A dict of headers to be used by `requests`.
        :param verify: Verify SSL certificate.
        :param proxies: The `proxies` argument will be passed to `requests`.
        :param kwargs: Extra parameters to include in the token request.
        :return: A token dict
        """
        if not token_url:
            raise ValueError("No token endpoint set for auto_refresh.")

        if not is_secure_transport(token_url):
            raise InsecureTransportError()

        refresh_token = refresh_token or self.token.get("refresh_token")

        log.debug(
            "Adding auto refresh key word arguments %s.", self.auto_refresh_kwargs
        )
        kwargs.update(self.auto_refresh_kwargs)
        body = self._client.prepare_refresh_body(
            body=body, refresh_token=refresh_token, scope=self.scope, **kwargs
        )
        log.debug("Prepared refresh token request body %s", body)

        if headers is None:
            headers = {
                "Accept": "application/json",
                "Content-Type": ("application/x-www-form-urlencoded;charset=UTF-8"),
            }

        r = self.post(
            token_url,
            data=dict(urldecode(body)),
            auth=auth,
            timeout=timeout,
            headers=headers,
            verify=verify,
            withhold_token=True,
            proxies=proxies,
        )
        log.debug("Request to refresh token completed with status %s.", r.status_code)
        log.debug("Response headers were %s and content %s.", r.headers, r.text)
        log.debug(
            "Invoking %d token response hooks.",
            len(self.compliance_hook["refresh_token_response"]),
        )
        for hook in self.compliance_hook["refresh_token_response"]:
            log.debug("Invoking hook %s.", hook)
            r = hook(r)

        self.token = self._client.parse_request_body_response(r.text, scope=self.scope)
        if not "refresh_token" in self.token:
            log.debug("No new refresh token given. Re-using old.")
            self.token["refresh_token"] = refresh_token
        return self.token