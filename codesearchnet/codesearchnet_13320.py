def make_kick_request(self,nick,reason):
        """
        Make the iq stanza a MUC room participant kick request.

        :Parameters:
            - `nick`: nickname of user to kick.
            - `reason`: reason of the kick.
        :Types:
            - `nick`: `unicode`
            - `reason`: `unicode`

        :return: object describing the kick request details.
        :returntype: `MucItem`
        """
        self.clear_muc_child()
        self.muc_child=MucAdminQuery(parent=self.xmlnode)
        item=MucItem("none","none",nick=nick,reason=reason)
        self.muc_child.add_item(item)
        return self.muc_child