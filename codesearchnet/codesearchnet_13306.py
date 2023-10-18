def __init(self,affiliation,role,jid=None,nick=None,actor=None,reason=None):
        """Initialize a `MucItem` object from a set of attributes.

        :Parameters:
            - `affiliation`: affiliation of the user.
            - `role`: role of the user.
            - `jid`: JID of the user.
            - `nick`: nickname of the user.
            - `actor`: actor modyfying the user data.
            - `reason`: reason of change of the user data.
        :Types:
            - `affiliation`: `str`
            - `role`: `str`
            - `jid`: `JID`
            - `nick`: `unicode`
            - `actor`: `JID`
            - `reason`: `unicode`
        """
        if not affiliation:
            affiliation=None
        elif affiliation not in affiliations:
            raise ValueError("Bad affiliation")
        self.affiliation=affiliation
        if not role:
            role=None
        elif role not in roles:
            raise ValueError("Bad role")
        self.role=role
        if jid:
            self.jid=JID(jid)
        else:
            self.jid=None
        if actor:
            self.actor=JID(actor)
        else:
            self.actor=None
        self.nick=nick
        self.reason=reason