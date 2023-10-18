def getPublicKey(registry=None):
    ''' Return the user's public key (generating and saving a new key pair if necessary) '''
    registry = registry or Registry_Base_URL
    pubkey_pem = None
    if _isPublicRegistry(registry):
        pubkey_pem = settings.getProperty('keys', 'public')
    else:
        for s in _getSources():
            if _sourceMatches(s, registry):
                if 'keys' in s and s['keys'] and 'public' in s['keys']:
                    pubkey_pem = s['keys']['public']
                    break
    if not pubkey_pem:
        pubkey_pem, privatekey_pem = _generateAndSaveKeys()
    else:
        # settings are unicode, we should be able to safely decode to ascii for
        # the key though, as it will either be hex or PEM encoded:
        pubkey_pem = pubkey_pem.encode('ascii')
    # if the key doesn't look like PEM, it might be hex-encided-DER (which we
    # used historically), so try loading that:
    if b'-----BEGIN PUBLIC KEY-----' in pubkey_pem:
        pubkey = serialization.load_pem_public_key(pubkey_pem, default_backend())
    else:
        pubkey_der = binascii.unhexlify(pubkey_pem)
        pubkey = serialization.load_der_public_key(pubkey_der, default_backend())
    return _pubkeyWireFormat(pubkey)