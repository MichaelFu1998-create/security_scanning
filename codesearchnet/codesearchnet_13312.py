def clear(self):
        """
        Clear the content of `self.xmlnode` removing all <item/>, <status/>, etc.
        """
        if not self.xmlnode.children:
            return
        n=self.xmlnode.children
        while n:
            ns=n.ns()
            if ns and ns.getContent()!=MUC_USER_NS:
                pass
            else:
                n.unlinkNode()
                n.freeNode()
            n=n.next