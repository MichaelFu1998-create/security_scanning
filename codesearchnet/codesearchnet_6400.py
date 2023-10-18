def intercom_user_hash(data):
    """
    Return a SHA-256 HMAC `user_hash` as expected by Intercom, if configured.

    Return None if the `INTERCOM_HMAC_SECRET_KEY` setting is not configured.
    """
    if getattr(settings, 'INTERCOM_HMAC_SECRET_KEY', None):
        return hmac.new(
            key=_hashable_bytes(settings.INTERCOM_HMAC_SECRET_KEY),
            msg=_hashable_bytes(data),
            digestmod=hashlib.sha256,
        ).hexdigest()
    else:
        return None