def get_jids(self):
        """Return JIDs for which this certificate is valid (except the domain
        wildcards).

        :Returtype: `list` of `JID`
        """
        result = []
        if ("XmppAddr" in self.alt_names or "DNS" in self.alt_names
                                            or "SRVName" in self.alt_names):
            addrs =  self.alt_names.get("XmppAddr", [])
            addrs += [ addr for addr in self.alt_names.get("DNS", [])
                                            if not addr.startswith("*.") ]
            addrs += [ addr.split(".", 1)[1] for addr
                                        in self.alt_names.get("SRVName", [])
                            if (addr.startswith("_xmpp-server.")
                                    or addr.startswith("_xmpp-client."))]
            warn_bad = True
        elif self.common_names:
            addrs = [addr for addr in self.common_names
                                if "@" not in addr and "/" not in addr]
            warn_bad = False
        else:
            return []
        for addr in addrs:
            try:
                jid = JID(addr)
                if jid not in result:
                    result.append(jid)
            except JIDError, err:
                if warn_bad:
                    logger.warning(u"Bad JID in the certificate: {0!r}: {1}"
                                                            .format(addr, err))
        return result