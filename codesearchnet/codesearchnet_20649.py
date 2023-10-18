def select(endpoint, cert=None, key=None, pem=None, ca=None, #pylint: disable=invalid-name, too-many-arguments
           aad=False, no_verify=False):
    #pylint: disable-msg=too-many-locals
    """
    Connects to a Service Fabric cluster endpoint.
    If connecting to secure cluster specify an absolute path to a cert (.crt)
    and key file (.key) or a single file with both (.pem). Do not specify both.
    Optionally, if connecting to a secure cluster, specify also an absolute
    path to a CA bundle file or directory of trusted CA certs.
    :param str endpoint: Cluster endpoint URL, including port and HTTP or HTTPS
    prefix
    :param str cert: Absolute path to a client certificate file
    :param str key: Absolute path to client certificate key file
    :param str pem: Absolute path to client certificate, as a .pem file
    :param str ca: Absolute path to CA certs directory to treat as valid
    or CA bundle
    file
    :param bool aad: Use Azure Active Directory for authentication
    :param bool no_verify: Disable verification for certificates when using
    HTTPS, note: this is an insecure option and should not be used for
    production environments
    """
    from sfctl.config import (set_ca_cert, set_auth, set_aad_cache,
                              set_cluster_endpoint,
                              set_no_verify)
    from msrest import ServiceClient, Configuration
    from sfctl.auth import ClientCertAuthentication, AdalAuthentication

    select_arg_verify(endpoint, cert, key, pem, ca, aad, no_verify)

    if aad:
        new_token, new_cache = get_aad_token(endpoint, no_verify)
        set_aad_cache(new_token, new_cache)
        rest_client = ServiceClient(
            AdalAuthentication(no_verify),
            Configuration(endpoint)
        )

        # Make sure basic GET request succeeds
        rest_client.send(rest_client.get('/')).raise_for_status()
    else:
        client_cert = None
        if pem:
            client_cert = pem
        elif cert:
            client_cert = (cert, key)

        rest_client = ServiceClient(
            ClientCertAuthentication(client_cert, ca, no_verify),
            Configuration(endpoint)
        )

        # Make sure basic GET request succeeds
        rest_client.send(rest_client.get('/')).raise_for_status()

    set_cluster_endpoint(endpoint)
    set_no_verify(no_verify)
    set_ca_cert(ca)
    set_auth(pem, cert, key, aad)