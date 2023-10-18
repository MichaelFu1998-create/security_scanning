def verify_jid_against_common_name(self, jid):
        """Return `True` if jid is listed in the certificate commonName.

        :Parameters:
            - `jid`: JID requested (domain part only)
        :Types:
            - `jid`: `JID`

        :Returntype: `bool`
        """
        if not self.common_names:
            return False
        for name in self.common_names:
            try:
                cn_jid = JID(name)
            except ValueError:
                continue
            if jid == cn_jid:
                return True
        return False