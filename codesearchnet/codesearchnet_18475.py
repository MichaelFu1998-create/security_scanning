def decode(secret: Union[str, bytes], token: Union[str, bytes],
           alg: str = default_alg) -> Tuple[dict, dict]:
    """
    Decodes the given token's header and payload and validates the signature.

    :param secret: The secret used to decode the token. Must match the
        secret used when creating the token.
    :type secret: Union[str, bytes]
    :param token: The token to decode.
    :type token: Union[str, bytes]
    :param alg: The algorithm used to decode the token. Must match the
        algorithm used when creating the token.
    :type alg: str
    :return: The decoded header and payload.
    :rtype: Tuple[dict, dict]
    """
    secret = util.to_bytes(secret)
    token = util.to_bytes(token)
    pre_signature, signature_segment = token.rsplit(b'.', 1)
    header_b64, payload_b64 = pre_signature.split(b'.')
    try:
        header_json = util.b64_decode(header_b64)
        header = json.loads(util.from_bytes(header_json))
    except (json.decoder.JSONDecodeError, UnicodeDecodeError, ValueError):
        raise InvalidHeaderError('Invalid header')
    try:
        payload_json = util.b64_decode(payload_b64)
        payload = json.loads(util.from_bytes(payload_json))
    except (json.decoder.JSONDecodeError, UnicodeDecodeError, ValueError):
        raise InvalidPayloadError('Invalid payload')

    if not isinstance(header, dict):
        raise InvalidHeaderError('Invalid header: {}'.format(header))
    if not isinstance(payload, dict):
        raise InvalidPayloadError('Invalid payload: {}'.format(payload))

    signature = util.b64_decode(signature_segment)
    calculated_signature = _hash(secret, pre_signature, alg)

    if not compare_signature(signature, calculated_signature):
        raise InvalidSignatureError('Invalid signature')
    return header, payload