def verify_signed_jwt_with_certs(jwt, certs, audience=None):
    """Verify a JWT against public certs.

    See http://self-issued.info/docs/draft-jones-json-web-token.html.

    Args:
        jwt: string, A JWT.
        certs: dict, Dictionary where values of public keys in PEM format.
        audience: string, The audience, 'aud', that this JWT should contain. If
                  None then the JWT's 'aud' parameter is not verified.

    Returns:
        dict, The deserialized JSON payload in the JWT.

    Raises:
        AppIdentityError: if any checks are failed.
    """
    jwt = _helpers._to_bytes(jwt)

    if jwt.count(b'.') != 2:
        raise AppIdentityError(
            'Wrong number of segments in token: {0}'.format(jwt))

    header, payload, signature = jwt.split(b'.')
    message_to_sign = header + b'.' + payload
    signature = _helpers._urlsafe_b64decode(signature)

    # Parse token.
    payload_bytes = _helpers._urlsafe_b64decode(payload)
    try:
        payload_dict = json.loads(_helpers._from_bytes(payload_bytes))
    except:
        raise AppIdentityError('Can\'t parse token: {0}'.format(payload_bytes))

    # Verify that the signature matches the message.
    _verify_signature(message_to_sign, signature, certs.values())

    # Verify the issued at and created times in the payload.
    _verify_time_range(payload_dict)

    # Check audience.
    _check_audience(payload_dict, audience)

    return payload_dict