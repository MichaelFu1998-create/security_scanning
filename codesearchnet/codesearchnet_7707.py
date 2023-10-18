def _make_request(self, service, method, params=None, body="",
                      need_auth=True):
        """Make an API request to the router."""
        # If we have no cookie (v2) or never called login before (v1)
        # and we need auth, the request will fail for sure.
        if need_auth and not self.cookie:
            if not self.login():
                return False, None

        headers = self._get_headers(service, method, need_auth)

        if not body:
            if not params:
                params = ""
            if isinstance(params, dict):
                _map = params
                params = ""
                for k in _map:
                    params += "<" + k + ">" + _map[k] + "</" + k + ">\n"

            body = CALL_BODY.format(service=SERVICE_PREFIX + service,
                                    method=method, params=params)

        message = SOAP_REQUEST.format(session_id=SESSION_ID, body=body)

        try:
            response = requests.post(self.soap_url, headers=headers,
                                     data=message, timeout=30, verify=False)

            if need_auth and _is_unauthorized_response(response):
                # let's discard the cookie because it probably expired (v2)
                # or the IP-bound (?) session expired (v1)
                self.cookie = None

                _LOGGER.warning("Unauthorized response, let's login and retry...")
                if self.login():
                    # reset headers with new cookie first
                    headers = self._get_headers(service, method, need_auth)
                    response = requests.post(self.soap_url, headers=headers,
                                             data=message, timeout=30, verify=False)

            success = _is_valid_response(response)

            if not success:
                _LOGGER.error("Invalid response")
                _LOGGER.debug("%s\n%s\n%s", response.status_code, str(response.headers), response.text)

            return success, response

        except requests.exceptions.RequestException:
            _LOGGER.exception("Error talking to API")

            # Maybe one day we will distinguish between
            # different errors..
            return False, None