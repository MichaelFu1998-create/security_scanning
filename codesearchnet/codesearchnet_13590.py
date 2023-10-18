def __from_unicode(cls, data, check = True):
        """Return jid tuple from an Unicode string.

        :Parameters:
            - `data`: the JID string
            - `check`: when `False` then the JID is not checked for
              specification compliance.

        :Return: (localpart, domainpart, resourcepart) tuple"""
        parts1 = data.split(u"/", 1)
        parts2 = parts1[0].split(u"@", 1)
        if len(parts2) == 2:
            local = parts2[0]
            domain = parts2[1]
            if check:
                local = cls.__prepare_local(local)
                domain = cls.__prepare_domain(domain)
        else:
            local = None
            domain = parts2[0]
            if check:
                domain = cls.__prepare_domain(domain)
        if len(parts1) == 2:
            resource = parts1[1]
            if check:
                resource = cls.__prepare_resource(parts1[1])
        else:
            resource = None
        if not domain:
            raise JIDError("Domain is required in JID.")
        return (local, domain, resource)