def verify_server(self, server_name, srv_type = 'xmpp-client'):
        """Verify certificate for a server.

        :Parameters:
            - `server_name`: name of the server presenting the cerificate
            - `srv_type`: service type requested, as used in the SRV record
        :Types:
            - `server_name`: `unicode` or `JID`
            - `srv_type`: `unicode`

        :Return: `True` if the certificate is valid for given name, `False`
        otherwise.
        """
        server_jid = JID(server_name)
        if "XmppAddr" not in self.alt_names and "DNS" not in self.alt_names \
                                and "SRV" not in self.alt_names:
            return self.verify_jid_against_common_name(server_jid)
        names = [name for name in self.alt_names.get("DNS", [])
                                        if not name.startswith(u"*.")]
        names += self.alt_names.get("XmppAddr", [])
        for name in names:
            logger.debug("checking {0!r} against {1!r}".format(server_jid,
                                                                name))
            try:
                jid = JID(name)
            except ValueError:
                logger.debug("Not a valid JID: {0!r}".format(name))
                continue
            if jid == server_jid:
                logger.debug("Match!")
                return True
        if srv_type and self.verify_jid_against_srv_name(server_jid, srv_type):
            return True
        wildcards = [name[2:] for name in self.alt_names.get("DNS", [])
                                                if name.startswith("*.")]
        if not wildcards or not "." in server_jid.domain:
            return False
        logger.debug("checking {0!r} against wildcard domains: {1!r}"
                                                .format(server_jid, wildcards))
        server_domain = JID(domain = server_jid.domain.split(".", 1)[1])
        for domain in wildcards:
            logger.debug("checking {0!r} against {1!r}".format(server_domain,
                                                                domain))
            try:
                jid = JID(domain)
            except ValueError:
                logger.debug("Not a valid JID: {0!r}".format(name))
                continue
            if jid == server_domain:
                logger.debug("Match!")
                return True
        return False