def encode(secret: Union[str, bytes], payload: dict = None,
           alg: str = default_alg, header: dict = None) -> str:
    """
    :param secret: The secret used to encode the token.
    :type secret: Union[str, bytes]
    :param payload: The payload to be encoded in the token.
    :type payload: dict
    :param alg: The algorithm used to hash the token.
    :type alg: str
    :param header: The header to be encoded in the token.
    :type header: dict
    :return: A new token
    :rtype: str
    """
    secret = util.to_bytes(secret)

    payload = payload or {}
    header = header or {}

    header_json = util.to_bytes(json.dumps(header))
    header_b64 = util.b64_encode(header_json)
    payload_json = util.to_bytes(json.dumps(payload))
    payload_b64 = util.b64_encode(payload_json)

    pre_signature = util.join(header_b64, payload_b64)
    signature = _hash(secret, pre_signature, alg)
    signature_b64 = util.b64_encode(signature)

    token = util.join(pre_signature, signature_b64)
    return util.from_bytes(token)