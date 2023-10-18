def update_presence(self,presence):
        """
        Update user information.

        :Parameters:
            - `presence`: a presence stanza with user information update.
        :Types:
            - `presence`: `MucPresence`
        """
        self.presence=MucPresence(presence)
        t=presence.get_type()
        if t=="unavailable":
            self.role="none"
            self.affiliation="none"
        self.room_jid=self.presence.get_from()
        self.nick=self.room_jid.resource
        mc=self.presence.get_muc_child()
        if isinstance(mc,MucUserX):
            items=mc.get_items()
            for item in items:
                if not isinstance(item,MucItem):
                    continue
                if item.role:
                    self.role=item.role
                if item.affiliation:
                    self.affiliation=item.affiliation
                if item.jid:
                    self.real_jid=item.jid
                if item.nick:
                    self.new_nick=item.nick
                break