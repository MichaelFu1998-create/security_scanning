def authenticate(username, password, service='login', encoding='utf-8',
                 resetcred=True):
    """Returns True if the given username and password authenticate for the
    given service.  Returns False otherwise.

    ``username``: the username to authenticate

    ``password``: the password in plain text

    ``service``: the PAM service to authenticate against.
                 Defaults to 'login'

    The above parameters can be strings or bytes.  If they are strings,
    they will be encoded using the encoding given by:

    ``encoding``: the encoding to use for the above parameters if they
                  are given as strings.  Defaults to 'utf-8'

    ``resetcred``: Use the pam_setcred() function to
                   reinitialize the credentials.
                   Defaults to 'True'.
    """

    if sys.version_info >= (3,):
        if isinstance(username, str):
            username = username.encode(encoding)
        if isinstance(password, str):
            password = password.encode(encoding)
        if isinstance(service, str):
            service = service.encode(encoding)

    @conv_func
    def my_conv(n_messages, messages, p_response, app_data):
        """Simple conversation function that responds to any
        prompt where the echo is off with the supplied password"""
        # Create an array of n_messages response objects
        addr = calloc(n_messages, sizeof(PamResponse))
        p_response[0] = cast(addr, POINTER(PamResponse))
        for i in range(n_messages):
            if messages[i].contents.msg_style == PAM_PROMPT_ECHO_OFF:
                pw_copy = strdup(password)
                p_response.contents[i].resp = cast(pw_copy, c_char_p)
                p_response.contents[i].resp_retcode = 0
        return 0

    handle = PamHandle()
    conv = PamConv(my_conv, 0)
    retval = pam_start(service, username, byref(conv), byref(handle))

    if retval != 0:
        # TODO: This is not an authentication error, something
        # has gone wrong starting up PAM
        return False

    retval = pam_authenticate(handle, 0)
    auth_success = (retval == 0)

    # Re-initialize credentials (for Kerberos users, etc)
    # Don't check return code of pam_setcred(), it shouldn't matter
    # if this fails
    if auth_success and resetcred:
        retval = pam_setcred(handle, PAM_REINITIALIZE_CRED)

    pam_end(handle, retval)

    return auth_success