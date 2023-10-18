def get_identities(self):
        """List the identity objects contained in `self`.

        :return: the list of identities.
        :returntype: `list` of `DiscoIdentity`"""
        ret=[]
        l=self.xpath_ctxt.xpathEval("d:identity")
        if l is not None:
            for i in l:
                ret.append(DiscoIdentity(self,i))
        return ret