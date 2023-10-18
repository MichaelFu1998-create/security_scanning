def decode(secret: Union[str, bytes], token: Union[str, bytes],
               alg: str = default_alg) -> 'Jwt':
        """
        Decodes the given token into an instance of `Jwt`.

        :param secret: The secret used to decode the token. Must match the
            secret used when creating the token.
        :type secret: Union[str, bytes]
        :param token: The token to decode.
        :type token: Union[str, bytes]
        :param alg: The algorithm used to decode the token. Must match the
            algorithm used when creating the token.
        :type alg: str
        :return: The decoded token.
        :rtype: `Jwt`
        """
        header, payload = decode(secret, token, alg)
        return Jwt(secret, payload, alg, header)