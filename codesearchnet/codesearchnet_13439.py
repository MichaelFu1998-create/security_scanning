def verify_client(self, client_jid = None, domains = None):
        """Verify certificate for a client.

        Please note that `client_jid` is only a hint to choose from the names,
        other JID may be returned if `client_jid` is not included in the
        certificate.

        :Parameters:
            - `client_jid`: client name requested. May be `None` to allow
              any name in one of the `domains`.
            - `domains`: list of domains we can handle.
        :Types:
            - `client_jid`: `JID`
            - `domains`: `list` of `unicode`

        :Return: one of the jids in the certificate or `None` is no authorized
        name is found.
        """
        jids = [jid for jid in self.get_jids() if jid.local]
        if not jids:
            return None
        if client_jid is not None and client_jid in jids:
            return client_jid
        if domains is None:
            return jids[0]
        for jid in jids:
            for domain in domains:
                if are_domains_equal(jid.domain, domain):
                    return jid
        return None