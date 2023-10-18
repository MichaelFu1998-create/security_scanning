def login(email=None, password=None, api_key=None, application='Default',
          url=None, verify_ssl_certificate=True):
    """
    Do the legwork of logging into the Midas Server instance, storing the API
    key and token.

    :param email: (optional) Email address to login with. If not set, the
        console will be prompted.
    :type email: None | string
    :param password: (optional) User password to login with. If not set and no
        'api_key' is set, the console will be prompted.
    :type password: None | string
    :param api_key: (optional) API key to login with. If not set, password
        login with be used.
    :type api_key: None | string
    :param application: (optional) Application name to be used with 'api_key'.
    :type application: string
    :param url: (optional) URL address of the Midas Server instance to login
        to. If not set, the console will be prompted.
    :type url: None | string
    :param verify_ssl_certificate: (optional) If True, the SSL certificate will
        be verified
    :type verify_ssl_certificate: bool
    :returns: API token.
    :rtype: string
    """
    try:
        input_ = raw_input
    except NameError:
        input_ = input

    if url is None:
        url = input_('Server URL: ')
    url = url.rstrip('/')
    if session.communicator is None:
        session.communicator = Communicator(url)
    else:
        session.communicator.url = url

    session.communicator.verify_ssl_certificate = verify_ssl_certificate

    if email is None:
        email = input_('Email: ')
    session.email = email

    if api_key is None:
        if password is None:
            password = getpass.getpass()
        session.api_key = session.communicator.get_default_api_key(
            session.email, password)
        session.application = 'Default'
    else:
        session.api_key = api_key
        session.application = application

    return renew_token()