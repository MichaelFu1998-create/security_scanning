def _load_client_secrets(filename):
    """Loads client secrets from the given filename.

    Args:
        filename: The name of the file containing the JSON secret key.

    Returns:
        A 2-tuple, the first item containing the client id, and the second
        item containing a client secret.
    """
    client_type, client_info = clientsecrets.loadfile(filename)

    if client_type != clientsecrets.TYPE_WEB:
        raise ValueError(
            'The flow specified in {} is not supported, only the WEB flow '
            'type  is supported.'.format(client_type))
    return client_info['client_id'], client_info['client_secret']