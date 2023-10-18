def maybe_key_vault(client, mount_path):
    """
    Set up a client key in Vault if one does not exist already.

    :param client:
        The Vault API client to use.
    :param mount_path:
        The Vault key/value mount path to use.
    :rtype: twisted.internet.defer.Deferred
    """
    d = client.read_kv2('client_key', mount_path=mount_path)

    def get_or_create_key(client_key):
        if client_key is not None:
            key_data = client_key['data']['data']
            key = _load_pem_private_key_bytes(key_data['key'].encode('utf-8'))
            return JWKRSA(key=key)
        else:
            key = generate_private_key(u'rsa')
            key_data = {
                'key': _dump_pem_private_key_bytes(key).decode('utf-8')
            }
            d = client.create_or_update_kv2(
                'client_key', key_data, mount_path=mount_path)

            return d.addCallback(lambda _result: JWKRSA(key=key))

    return d.addCallback(get_or_create_key)