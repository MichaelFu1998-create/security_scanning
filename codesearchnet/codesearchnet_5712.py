def _extract_id_token(id_token):
    """Extract the JSON payload from a JWT.

    Does the extraction w/o checking the signature.

    Args:
        id_token: string or bytestring, OAuth 2.0 id_token.

    Returns:
        object, The deserialized JSON payload.
    """
    if type(id_token) == bytes:
        segments = id_token.split(b'.')
    else:
        segments = id_token.split(u'.')

    if len(segments) != 3:
        raise VerifyJwtTokenError(
            'Wrong number of segments in token: {0}'.format(id_token))

    return json.loads(
        _helpers._from_bytes(_helpers._urlsafe_b64decode(segments[1])))