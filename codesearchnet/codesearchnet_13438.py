def verify_jid_against_srv_name(self, jid, srv_type):
        """Check if the cerificate is valid for given domain-only JID
        and a service type.

        :Parameters:
            - `jid`: JID requested (domain part only)
            - `srv_type`: service type, e.g. 'xmpp-client'
        :Types:
            - `jid`: `JID`
            - `srv_type`: `unicode`
        :Returntype: `bool`
        """
        srv_prefix = u"_" + srv_type + u"."
        srv_prefix_l = len(srv_prefix)
        for srv in self.alt_names.get("SRVName", []):
            logger.debug("checking {0!r} against {1!r}".format(jid,
                                                                srv))
            if not srv.startswith(srv_prefix):
                logger.debug("{0!r} does not start with {1!r}"
                                                .format(srv, srv_prefix))
                continue
            try:
                srv_jid = JID(srv[srv_prefix_l:])
            except ValueError:
                continue
            if srv_jid == jid:
                logger.debug("Match!")
                return True
        return False