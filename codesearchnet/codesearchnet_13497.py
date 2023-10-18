def get_items(self):
        """Get the items contained in `self`.

        :return: the items contained.
        :returntype: `list` of `DiscoItem`"""
        ret=[]
        l=self.xpath_ctxt.xpathEval("d:item")
        if l is not None:
            for i in l:
                ret.append(DiscoItem(self, i))
        return ret