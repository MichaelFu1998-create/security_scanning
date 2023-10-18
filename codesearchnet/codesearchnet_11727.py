def apt_key_exists(keyid):
    """
    Check if the given key id exists in apt keyring.
    """

    # Command extracted from apt-key source
    gpg_cmd = 'gpg --ignore-time-conflict --no-options --no-default-keyring --keyring /etc/apt/trusted.gpg'

    with settings(hide('everything'), warn_only=True):
        res = run('%(gpg_cmd)s --fingerprint %(keyid)s' % locals())

    return res.succeeded