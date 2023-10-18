def _compute_response(urp_hash, nonce, cnonce, nonce_count, authzid,
                                                                    digest_uri):
    """Compute DIGEST-MD5 response value.

    :Parameters:
        - `urp_hash`: MD5 sum of username:realm:password.
        - `nonce`: nonce value from a server challenge.
        - `cnonce`: cnonce value from the client response.
        - `nonce_count`: nonce count value.
        - `authzid`: authorization id.
        - `digest_uri`: digest-uri value.
    :Types:
        - `urp_hash`: `bytes`
        - `nonce`: `bytes`
        - `nonce_count`: `int`
        - `authzid`: `bytes`
        - `digest_uri`: `bytes`

    :return: the computed response value.
    :returntype: `bytes`"""
    # pylint: disable-msg=C0103,R0913
    logger.debug("_compute_response{0!r}".format((urp_hash, nonce, cnonce,
                                            nonce_count, authzid,digest_uri)))
    if authzid:
        a1 = b":".join((urp_hash, nonce, cnonce, authzid))
    else:
        a1 = b":".join((urp_hash, nonce, cnonce))
    a2 = b"AUTHENTICATE:" + digest_uri
    return b2a_hex(_kd_value(b2a_hex(_h_value(a1)), b":".join((
            nonce, nonce_count, cnonce, b"auth", b2a_hex(_h_value(a2))))))