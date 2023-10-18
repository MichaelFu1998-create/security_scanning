def get_token(http, service_account='default'):
    """Fetch an oauth token for the

    Args:
        http: an object to be used to make HTTP requests.
        service_account: An email specifying the service account this token
            should represent. Default will be a token for the "default" service
            account of the current compute engine instance.

    Returns:
         A tuple of (access token, token expiration), where access token is the
         access token as a string and token expiration is a datetime object
         that indicates when the access token will expire.
    """
    token_json = get(
        http,
        'instance/service-accounts/{0}/token'.format(service_account))
    token_expiry = client._UTCNOW() + datetime.timedelta(
        seconds=token_json['expires_in'])
    return token_json['access_token'], token_expiry