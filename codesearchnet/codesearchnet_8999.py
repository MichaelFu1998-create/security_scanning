def connect(host='localhost', port=8080, ssl_verify=False, ssl_key=None,
            ssl_cert=None, timeout=10, protocol=None, url_path='/',
            username=None, password=None, token=None):
    """Connect with PuppetDB. This will return an object allowing you
    to query the API through its methods.

    :param host: (Default: 'localhost;) Hostname or IP of PuppetDB.
    :type host: :obj:`string`

    :param port: (Default: '8080') Port on which to talk to PuppetDB.
    :type port: :obj:`int`

    :param ssl_verify: (optional) Verify PuppetDB server certificate.
    :type ssl_verify: :obj:`bool` or :obj:`string` True, False or filesystem \
            path to CA certificate.

    :param ssl_key: (optional) Path to our client secret key.
    :type ssl_key: :obj:`None` or :obj:`string` representing a filesystem\
            path.

    :param ssl_cert: (optional) Path to our client certificate.
    :type ssl_cert: :obj:`None` or :obj:`string` representing a filesystem\
            path.

    :param timeout: (Default: 10) Number of seconds to wait for a response.
    :type timeout: :obj:`int`

    :param protocol: (optional) Explicitly specify the protocol to be used
            (especially handy when using HTTPS with ssl_verify=False and
            without certs)
    :type protocol: :obj:`None` or :obj:`string`

    :param url_path: (Default: '/') The URL path where PuppetDB is served
    :type url_path: :obj:`None` or :obj:`string`

    :param username: (optional) The username to use for HTTP basic
            authentication
    :type username: :obj:`None` or :obj:`string`

    :param password: (optional) The password to use for HTTP basic
            authentication
    :type password: :obj:`None` or :obj:`string`

    :param token: (optional) The x-auth token to use for X-Authentication
    :type token: :obj:`None` or :obj:`string`
    """
    return BaseAPI(host=host, port=port,
                   timeout=timeout, ssl_verify=ssl_verify, ssl_key=ssl_key,
                   ssl_cert=ssl_cert, protocol=protocol, url_path=url_path,
                   username=username, password=password, token=token)