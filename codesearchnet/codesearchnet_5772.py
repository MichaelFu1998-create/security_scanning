def xsrf_secret_key():
    """Return the secret key for use for XSRF protection.

    If the Site entity does not have a secret key, this method will also create
    one and persist it.

    Returns:
        The secret key.
    """
    secret = memcache.get(XSRF_MEMCACHE_ID, namespace=OAUTH2CLIENT_NAMESPACE)
    if not secret:
        # Load the one and only instance of SiteXsrfSecretKey.
        model = SiteXsrfSecretKey.get_or_insert(key_name='site')
        if not model.secret:
            model.secret = _generate_new_xsrf_secret_key()
            model.put()
        secret = model.secret
        memcache.add(XSRF_MEMCACHE_ID, secret,
                     namespace=OAUTH2CLIENT_NAMESPACE)

    return str(secret)