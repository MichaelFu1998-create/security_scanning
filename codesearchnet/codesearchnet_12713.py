async def get_oauth_verifier(oauth_token):
    """
    Open authorize page in a browser,
    print the url if it didn't work

    Arguments
    ---------
    oauth_token : str
        The oauth token received in :func:`get_oauth_token`

    Returns
    -------
    str
        The PIN entered by the user
    """
    url = "https://api.twitter.com/oauth/authorize?oauth_token=" + oauth_token

    try:
        browser = webbrowser.open(url)
        await asyncio.sleep(2)

        if not browser:
            raise RuntimeError
    except RuntimeError:
        print("could not open a browser\ngo here to enter your PIN: " + url)

    verifier = input("\nEnter your PIN: ")
    return verifier