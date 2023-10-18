def add_apt_key(filename=None, url=None, keyid=None, keyserver='subkeys.pgp.net', update=False):
    """
    Trust packages signed with this public key.

    Example::

        import burlap

        # Varnish signing key from URL and verify fingerprint)
        burlap.deb.add_apt_key(keyid='C4DEFFEB', url='http://repo.varnish-cache.org/debian/GPG-key.txt')

        # Nginx signing key from default key server (subkeys.pgp.net)
        burlap.deb.add_apt_key(keyid='7BD9BF62')

        # From custom key server
        burlap.deb.add_apt_key(keyid='7BD9BF62', keyserver='keyserver.ubuntu.com')

        # From a file
        burlap.deb.add_apt_key(keyid='7BD9BF62', filename='nginx.asc'
    """

    if keyid is None:
        if filename is not None:
            run_as_root('apt-key add %(filename)s' % locals())
        elif url is not None:
            run_as_root('wget %(url)s -O - | apt-key add -' % locals())
        else:
            raise ValueError('Either filename, url or keyid must be provided as argument')
    else:
        if filename is not None:
            _check_pgp_key(filename, keyid)
            run_as_root('apt-key add %(filename)s' % locals())
        elif url is not None:
            tmp_key = '/tmp/tmp.burlap.key.%(keyid)s.key' % locals()
            run_as_root('wget %(url)s -O %(tmp_key)s' % locals())
            _check_pgp_key(tmp_key, keyid)
            run_as_root('apt-key add %(tmp_key)s' % locals())
        else:
            keyserver_opt = '--keyserver %(keyserver)s' % locals() if keyserver is not None else ''
            run_as_root('apt-key adv %(keyserver_opt)s --recv-keys %(keyid)s' % locals())

    if update:
        update_index()