def make_muc_admin_quey(self):
        """
        Create <query xmlns="...muc#admin"/> element in the stanza.

        :return: the element created.
        :returntype: `MucAdminQuery`
        """
        self.clear_muc_child()
        self.muc_child=MucAdminQuery(parent=self.xmlnode)
        return self.muc_child