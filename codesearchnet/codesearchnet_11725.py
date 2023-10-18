def preseed_package(pkg_name, preseed):
    """
    Enable unattended package installation by preseeding ``debconf``
    parameters.

    Example::

        import burlap

        # Unattended install of Postfix mail server
        burlap.deb.preseed_package('postfix', {
            'postfix/main_mailer_type': ('select', 'Internet Site'),
            'postfix/mailname': ('string', 'example.com'),
            'postfix/destinations': ('string', 'example.com, localhost.localdomain, localhost'),
        })
        burlap.deb.install('postfix')

    """
    for q_name, _ in preseed.items():
        q_type, q_answer = _
        run_as_root('echo "%(pkg_name)s %(q_name)s %(q_type)s %(q_answer)s" | debconf-set-selections' % locals())