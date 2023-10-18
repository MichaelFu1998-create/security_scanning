def _verify_time_range(payload_dict):
    """Verifies the issued at and expiration from a JWT payload.

    Makes sure the current time (in UTC) falls between the issued at and
    expiration for the JWT (with some skew allowed for via
    ``CLOCK_SKEW_SECS``).

    Args:
        payload_dict: dict, A dictionary containing a JWT payload.

    Raises:
        AppIdentityError: If there is no ``'iat'`` field in the payload
                          dictionary.
        AppIdentityError: If there is no ``'exp'`` field in the payload
                          dictionary.
        AppIdentityError: If the JWT expiration is too far in the future (i.e.
                          if the expiration would imply a token lifetime
                          longer than what is allowed.)
        AppIdentityError: If the token appears to have been issued in the
                          future (up to clock skew).
        AppIdentityError: If the token appears to have expired in the past
                          (up to clock skew).
    """
    # Get the current time to use throughout.
    now = int(time.time())

    # Make sure issued at and expiration are in the payload.
    issued_at = payload_dict.get('iat')
    if issued_at is None:
        raise AppIdentityError(
            'No iat field in token: {0}'.format(payload_dict))
    expiration = payload_dict.get('exp')
    if expiration is None:
        raise AppIdentityError(
            'No exp field in token: {0}'.format(payload_dict))

    # Make sure the expiration gives an acceptable token lifetime.
    if expiration >= now + MAX_TOKEN_LIFETIME_SECS:
        raise AppIdentityError(
            'exp field too far in future: {0}'.format(payload_dict))

    # Make sure (up to clock skew) that the token wasn't issued in the future.
    earliest = issued_at - CLOCK_SKEW_SECS
    if now < earliest:
        raise AppIdentityError('Token used too early, {0} < {1}: {2}'.format(
            now, earliest, payload_dict))
    # Make sure (up to clock skew) that the token isn't already expired.
    latest = expiration + CLOCK_SKEW_SECS
    if now > latest:
        raise AppIdentityError('Token used too late, {0} > {1}: {2}'.format(
            now, latest, payload_dict))