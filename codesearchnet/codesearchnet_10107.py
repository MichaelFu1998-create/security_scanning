def raise_hostname(certificate, hostname):
    """
    Raises a TLSVerificationError due to a hostname mismatch

    :param certificate:
        An asn1crypto.x509.Certificate object

    :raises:
        TLSVerificationError
    """

    is_ip = re.match('^\\d+\\.\\d+\\.\\d+\\.\\d+$', hostname) or hostname.find(':') != -1
    if is_ip:
        hostname_type = 'IP address %s' % hostname
    else:
        hostname_type = 'domain name %s' % hostname
    message = 'Server certificate verification failed - %s does not match' % hostname_type
    valid_ips = ', '.join(certificate.valid_ips)
    valid_domains = ', '.join(certificate.valid_domains)
    if valid_domains:
        message += ' valid domains: %s' % valid_domains
    if valid_domains and valid_ips:
        message += ' or'
    if valid_ips:
        message += ' valid IP addresses: %s' % valid_ips
    raise TLSVerificationError(message, certificate)