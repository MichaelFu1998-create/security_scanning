def clear_muc_child(self):
        """
        Remove the MUC specific stanza payload element.
        """
        if self.muc_child:
            self.muc_child.free_borrowed()
            self.muc_child=None
        if not self.xmlnode.children:
            return
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
            if ns_uri in (MUC_NS,MUC_USER_NS,MUC_ADMIN_NS,MUC_OWNER_NS):
                n.unlinkNode()
                n.freeNode()
            n=n.next