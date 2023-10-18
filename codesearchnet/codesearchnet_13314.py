def get_muc_child(self):
        """
        Get the MUC specific payload element.

        :return: the object describing the stanza payload in MUC namespace.
        :returntype: `MucX` or `MucUserX` or `MucAdminQuery` or `MucOwnerX`
        """
        if self.muc_child:
            return self.muc_child
        if not self.xmlnode.children:
            return None
        n=self.xmlnode.children
        while n:
            if n.name not in ("x","query"):
                n=n.next
                continue
            ns=n.ns()
            if not ns:
                n=n.next
                continue
            ns_uri=ns.getContent()
            if (n.name,ns_uri)==("x",MUC_NS):
                self.muc_child=MucX(n)
                return self.muc_child
            if (n.name,ns_uri)==("x",MUC_USER_NS):
                self.muc_child=MucUserX(n)
                return self.muc_child
            if (n.name,ns_uri)==("query",MUC_ADMIN_NS):
                self.muc_child=MucAdminQuery(n)
                return self.muc_child
            if (n.name,ns_uri)==("query",MUC_OWNER_NS):
                self.muc_child=MucOwnerX(n)
                return self.muc_child
            n=n.next