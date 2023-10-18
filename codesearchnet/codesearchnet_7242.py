def _get_authorization_code(session, credentials_prompt):
    """Get authorization code using Google account credentials.

    Because hangups can't use a real embedded browser, it has to use the
    Browser class to enter the user's credentials and retrieve the
    authorization code, which is placed in a cookie. This is the most fragile
    part of the authentication process, because a change to a login form or an
    unexpected prompt could break it.

    Raises GoogleAuthError authentication fails.

    Returns authorization code string.
    """
    browser = Browser(session, OAUTH2_LOGIN_URL)

    email = credentials_prompt.get_email()
    browser.submit_form(FORM_SELECTOR, {EMAIL_SELECTOR: email})

    password = credentials_prompt.get_password()
    browser.submit_form(FORM_SELECTOR, {PASSWORD_SELECTOR: password})

    if browser.has_selector(TOTP_CHALLENGE_SELECTOR):
        browser.submit_form(TOTP_CHALLENGE_SELECTOR, {})
    elif browser.has_selector(PHONE_CHALLENGE_SELECTOR):
        browser.submit_form(PHONE_CHALLENGE_SELECTOR, {})

    if browser.has_selector(VERIFICATION_FORM_SELECTOR):
        if browser.has_selector(TOTP_CODE_SELECTOR):
            input_selector = TOTP_CODE_SELECTOR
        elif browser.has_selector(PHONE_CODE_SELECTOR):
            input_selector = PHONE_CODE_SELECTOR
        else:
            raise GoogleAuthError('Unknown verification code input')
        verfification_code = credentials_prompt.get_verification_code()
        browser.submit_form(
            VERIFICATION_FORM_SELECTOR, {input_selector: verfification_code}
        )

    try:
        return browser.get_cookie('oauth_code')
    except KeyError:
        raise GoogleAuthError('Authorization code cookie not found')