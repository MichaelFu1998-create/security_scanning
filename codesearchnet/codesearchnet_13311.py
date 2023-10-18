def get_items(self):
        """Get a list of objects describing the content of `self`.

        :return: the list of objects.
        :returntype: `list` of `MucItemBase` (`MucItem` and/or `MucStatus`)
        """
        if not self.xmlnode.children:
            return []
        ret=[]
        n=self.xmlnode.children
        while n:
            ns=n.ns()
            if ns and ns.getContent()!=self.ns:
                pass
            elif n.name=="item":
                ret.append(MucItem(n))
            elif n.name=="status":
                ret.append(MucStatus(n))
            # FIXME: alt,decline,invite,password
            n=n.next
        return ret