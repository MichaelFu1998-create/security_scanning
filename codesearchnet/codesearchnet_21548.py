def create_jwt(integration_id, private_key_path):
    """Create a JSON Web Token to authenticate a GitHub Integration or
    installation.

    Parameters
    ----------
    integration_id : `int`
        Integration ID. This is available from the GitHub integration's
        homepage.
    private_key_path : `str`
        Path to the integration's private key (a ``.pem`` file).

    Returns
    -------
    jwt : `bytes`
        JSON Web Token that is good for 9 minutes.

    Notes
    -----
    The JWT is encoded with the RS256 algorithm. It includes a payload with
    fields:

    - ``'iat'``: The current time, as an `int` timestamp.
    - ``'exp'``: Expiration time, as an `int timestamp. The expiration
      time is set of 9 minutes in the future (maximum allowance is 10 minutes).
    - ``'iss'``: The integration ID (`int`).

    For more information, see
    https://developer.github.com/early-access/integrations/authentication/.
    """
    integration_id = int(integration_id)

    with open(private_key_path, 'rb') as f:
        cert_bytes = f.read()

    now = datetime.datetime.now()
    expiration_time = now + datetime.timedelta(minutes=9)
    payload = {
        # Issued at time
        'iat': int(now.timestamp()),
        # JWT expiration time (10 minute maximum)
        'exp': int(expiration_time.timestamp()),
        # Integration's GitHub identifier
        'iss': integration_id
    }

    return jwt.encode(payload, cert_bytes, algorithm='RS256')