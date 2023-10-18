def remove(self):
        """Remove `self` from the containing `DiscoItems` object."""
        if self.disco is None:
            return
        self.xmlnode.unlinkNode()
        oldns=self.xmlnode.ns()
        ns=self.xmlnode.newNs(oldns.getContent(),None)
        self.xmlnode.replaceNs(oldns,ns)
        common_root.addChild(self.xmlnode())
        self.disco=None