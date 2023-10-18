def remove_feature(self,var):
        """Remove a feature from `self`.

        :Parameters:
            - `var`: the feature name.
        :Types:
            - `var`: `unicode`"""
        if not var:
            raise ValueError("var is None")
        if '"' not in var:
            expr='d:feature[@var="%s"]' % (var,)
        elif "'" not in var:
            expr="d:feature[@var='%s']" % (var,)
        else:
            raise ValueError("Invalid feature name")

        l=self.xpath_ctxt.xpathEval(expr)
        if not l:
            return

        for f in l:
            f.unlinkNode()
            f.freeNode()