def check_version():
    """
    Compares the local version against the latest official version on PyPI and displays a warning message if a newer release is available.

    This check can be disabled by setting the environment variable BURLAP_CHECK_VERSION=0.
    """
    global CHECK_VERSION
    if not CHECK_VERSION:
        return
    # Ensure we only check once in this process.
    CHECK_VERSION = 0
    # Lookup most recent remote version.
    from six.moves.urllib.request import urlopen
    try:
        response = urlopen("https://pypi.org/pypi/burlap/json")
        data = json.loads(response.read().decode())
        remote_release = sorted(tuple(map(int, _.split('.'))) for _ in data['releases'].keys())[-1]
        remote_release_str = '.'.join(map(str, remote_release))
        local_release = VERSION
        local_release_str = '.'.join(map(str, local_release))
        # Display warning.
        if remote_release > local_release:
            print('\033[93m')
            print("You are using burlap version %s, however version %s is available." % (local_release_str, remote_release_str))
            print("You should consider upgrading via the 'pip install --upgrade burlap' command.")
            print('\033[0m')
    except Exception as exc:
        print('\033[93m')
        print("Unable to check for updated burlap version: %s" % exc)
        print('\033[0m')