def create_marathon_acme(
    client_creator, cert_store, acme_email, allow_multiple_certs,
    marathon_addrs, marathon_timeout, sse_timeout, mlb_addrs, group,
        reactor):
    """
    Create a marathon-acme instance.

    :param client_creator:
        The txacme client creator function.
    :param cert_store:
        The txacme certificate store instance.
    :param acme_email:
        Email address to use when registering with the ACME service.
    :param allow_multiple_certs:
        Whether to allow multiple certificates per app port.
    :param marathon_addr:
        Address for the Marathon instance to find app domains that require
        certificates.
    :param marathon_timeout:
        Amount of time in seconds to wait for response headers to be received
        from Marathon.
    :param sse_timeout:
        Amount of time in seconds to wait for some event data to be received
        from Marathon.
    :param mlb_addrs:
        List of addresses for marathon-lb instances to reload when a new
        certificate is issued.
    :param group:
        The marathon-lb group (``HAPROXY_GROUP``) to consider when finding
        app domains.
    :param reactor: The reactor to use.
    """
    marathon_client = MarathonClient(marathon_addrs, timeout=marathon_timeout,
                                     sse_kwargs={'timeout': sse_timeout},
                                     reactor=reactor)
    marathon_lb_client = MarathonLbClient(mlb_addrs, reactor=reactor)

    return MarathonAcme(
        marathon_client,
        group,
        cert_store,
        marathon_lb_client,
        client_creator,
        reactor,
        acme_email,
        allow_multiple_certs
    )