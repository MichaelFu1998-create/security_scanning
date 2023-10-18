def renew_token():
    """
    Renew or get a token to use for transactions with the Midas Server
    instance.

    :returns: API token.
    :rtype: string
    """
    session.token = session.communicator.login_with_api_key(
        session.email, session.api_key, application=session.application)
    if len(session.token) < 10:  # HACK to check for mfa being enabled
        one_time_pass = getpass.getpass('One-Time Password: ')
        session.token = session.communicator.mfa_otp_login(
            session.token, one_time_pass)
    return session.token