def __prepare_domain(data):
        """Prepare domainpart of the JID.

        :Parameters:
            - `data`: Domain part of the JID
        :Types:
            - `data`: `unicode`

        :raise JIDError: if the domain name is too long.
        """
        # pylint: disable=R0912
        if not data:
            raise JIDError("Domain must be given")
        data = unicode(data)
        if not data:
            raise JIDError("Domain must be given")
        if u'[' in data:
            if data[0] == u'[' and data[-1] == u']':
                try:
                    addr = _validate_ip_address(socket.AF_INET6, data[1:-1])
                    return "[{0}]".format(addr)
                except ValueError, err:
                    logger.debug("ValueError: {0}".format(err))
                    raise JIDError(u"Invalid IPv6 literal in JID domainpart")
            else:
                raise JIDError(u"Invalid use of '[' or ']' in JID domainpart")
        elif data[0].isdigit() and data[-1].isdigit():
            try:
                addr = _validate_ip_address(socket.AF_INET, data)
            except ValueError, err:
                logger.debug("ValueError: {0}".format(err))
        data = UNICODE_DOT_RE.sub(u".", data)
        data = data.rstrip(u".")
        labels = data.split(u".")
        try:
            labels = [idna.nameprep(label) for label in labels]
        except UnicodeError:
            raise JIDError(u"Domain name invalid")
        for label in labels:
            if not STD3_LABEL_RE.match(label):
                raise JIDError(u"Domain name invalid")
            try:
                idna.ToASCII(label)
            except UnicodeError:
                raise JIDError(u"Domain name invalid")
        domain = u".".join(labels)
        if len(domain.encode("utf-8")) > 1023:
            raise JIDError(u"Domain name too long")
        return domain