def check_password(self, username, password, properties):
        """Check the password validity.

        Used by plain-text authentication mechanisms.

        Default implementation: retrieve a "plain" password for the `username`
        and `realm` using `self.get_password` and compare it with the password
        provided.

        May be overridden e.g. to check the password against some external
        authentication mechanism (PAM, LDAP, etc.).

        :Parameters:
            - `username`: the username for which the password verification is
              requested.
            - `password`: the password to verify.
            - `properties`: mapping with authentication properties (those
              provided to the authenticator's ``start()`` method plus some
              already obtained via the mechanism).
        :Types:
            - `username`: `unicode`
            - `password`: `unicode`
            - `properties`: mapping

        :return: `True` if the password is valid.
        :returntype: `bool`
        """
        logger.debug("check_password{0!r}".format(
                                            (username, password, properties)))
        pwd, pwd_format = self.get_password(username,
                    (u"plain", u"md5:user:realm:password"), properties)
        if pwd_format == u"plain":
            logger.debug("got plain password: {0!r}".format(pwd))
            return pwd is not None and password == pwd
        elif pwd_format in (u"md5:user:realm:password"):
            logger.debug("got md5:user:realm:password password: {0!r}"
                                                            .format(pwd))
            realm = properties.get("realm")
            if realm is None:
                realm = ""
            else:
                realm = realm.encode("utf-8")
            username = username.encode("utf-8")
            password = password.encode("utf-8")

            # pylint: disable-msg=E1101
            urp_hash = hashlib.md5(b"%s:%s:%s").hexdigest()
            return urp_hash == pwd
        logger.debug("got password in unknown format: {0!r}".format(pwd_format))
        return False