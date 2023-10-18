def _cert_data_to_pem_objects(cert_data):
    """
    Given a non-None response from the Vault key/value store, convert the
    key/values into a list of PEM objects.
    """
    pem_objects = []
    for key in ['privkey', 'cert', 'chain']:
        pem_objects.extend(pem.parse(cert_data[key].encode('utf-8')))

    return pem_objects