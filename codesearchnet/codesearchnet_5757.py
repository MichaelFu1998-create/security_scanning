def wrap_http_for_jwt_access(credentials, http):
    """Prepares an HTTP object's request method for JWT access.

    Wraps HTTP requests with logic to catch auth failures (typically
    identified via a 401 status code). In the event of failure, tries
    to refresh the token used and then retry the original request.

    Args:
        credentials: _JWTAccessCredentials, the credentials used to identify
                     a service account that uses JWT access tokens.
        http: httplib2.Http, an http object to be used to make
              auth requests.
    """
    orig_request_method = http.request
    wrap_http_for_auth(credentials, http)
    # The new value of ``http.request`` set by ``wrap_http_for_auth``.
    authenticated_request_method = http.request

    # The closure that will replace 'httplib2.Http.request'.
    def new_request(uri, method='GET', body=None, headers=None,
                    redirections=httplib2.DEFAULT_MAX_REDIRECTS,
                    connection_type=None):
        if 'aud' in credentials._kwargs:
            # Preemptively refresh token, this is not done for OAuth2
            if (credentials.access_token is None or
                    credentials.access_token_expired):
                credentials.refresh(None)
            return request(authenticated_request_method, uri,
                           method, body, headers, redirections,
                           connection_type)
        else:
            # If we don't have an 'aud' (audience) claim,
            # create a 1-time token with the uri root as the audience
            headers = _initialize_headers(headers)
            _apply_user_agent(headers, credentials.user_agent)
            uri_root = uri.split('?', 1)[0]
            token, unused_expiry = credentials._create_token({'aud': uri_root})

            headers['Authorization'] = 'Bearer ' + token
            return request(orig_request_method, uri, method, body,
                           clean_headers(headers),
                           redirections, connection_type)

    # Replace the request method with our own closure.
    http.request = new_request

    # Set credentials as a property of the request method.
    http.request.credentials = credentials