def raise_expired_not_yet_valid(certificate):
    """
    Raises a TLSVerificationError due to certificate being expired, or not yet
    being valid

    :param certificate:
        An asn1crypto.x509.Certificate object

    :raises:
        TLSVerificationError
    """

    validity = certificate['tbs_certificate']['validity']
    not_after = validity['not_after'].native
    not_before = validity['not_before'].native

    now = datetime.now(timezone.utc)

    if not_before > now:
        formatted_before = not_before.strftime('%Y-%m-%d %H:%M:%SZ')
        message = 'Server certificate verification failed - certificate not valid until %s' % formatted_before
    elif not_after < now:
        formatted_after = not_after.strftime('%Y-%m-%d %H:%M:%SZ')
        message = 'Server certificate verification failed - certificate expired %s' % formatted_after

    raise TLSVerificationError(message, certificate)