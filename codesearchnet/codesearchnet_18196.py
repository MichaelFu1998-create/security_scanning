def maybe_key(pem_path):
    """
    Set up a client key if one does not exist already.

    https://gist.github.com/glyph/27867a478bb71d8b6046fbfb176e1a33#file-local-certs-py-L32-L50

    :type pem_path: twisted.python.filepath.FilePath
    :param pem_path:
        The path to the certificate directory to use.
    :rtype: twisted.internet.defer.Deferred
    """
    acme_key_file = pem_path.child(u'client.key')
    if acme_key_file.exists():
        key = _load_pem_private_key_bytes(acme_key_file.getContent())
    else:
        key = generate_private_key(u'rsa')
        acme_key_file.setContent(_dump_pem_private_key_bytes(key))
    return succeed(JWKRSA(key=key))