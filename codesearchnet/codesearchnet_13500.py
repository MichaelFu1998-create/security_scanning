def has_item(self,jid,node=None):
        """Check if `self` contains an item.

        :Parameters:
            - `jid`: JID of the item.
            - `node`: node name of the item.
        :Types:
            - `jid`: `JID`
            - `node`: `libxml2.xmlNode`

        :return: `True` if the item is found in `self`.
        :returntype: `bool`"""
        l=self.xpath_ctxt.xpathEval("d:item")
        if l is None:
            return False
        for it in l:
            di=DiscoItem(self,it)
            if di.jid==jid and di.node==node:
                return True
        return False