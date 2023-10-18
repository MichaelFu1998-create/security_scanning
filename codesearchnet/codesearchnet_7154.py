def _get_authorization_headers(sapisid_cookie):
    """Return authorization headers for API request."""
    # It doesn't seem to matter what the url and time are as long as they are
    # consistent.
    time_msec = int(time.time() * 1000)
    auth_string = '{} {} {}'.format(time_msec, sapisid_cookie, ORIGIN_URL)
    auth_hash = hashlib.sha1(auth_string.encode()).hexdigest()
    sapisidhash = 'SAPISIDHASH {}_{}'.format(time_msec, auth_hash)
    return {
        'authorization': sapisidhash,
        'x-origin': ORIGIN_URL,
        'x-goog-authuser': '0',
    }