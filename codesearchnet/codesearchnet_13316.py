def make_muc_userinfo(self):
        """
        Create <x xmlns="...muc#user"/> element in the stanza.

        :return: the element created.
        :returntype: `MucUserX`
        """
        self.clear_muc_child()
        self.muc_child=MucUserX(parent=self.xmlnode)
        return self.muc_child