def has_feature(self,var):
        """Check if `self` contains the named feature.

        :Parameters:
            - `var`: the feature name.
        :Types:
            - `var`: `unicode`

        :return: `True` if the feature is found in `self`.
        :returntype: `bool`"""
        if not var:
            raise ValueError("var is None")
        if '"' not in var:
            expr=u'd:feature[@var="%s"]' % (var,)
        elif "'" not in var:
            expr=u"d:feature[@var='%s']" % (var,)
        else:
            raise ValueError("Invalid feature name")

        l=self.xpath_ctxt.xpathEval(to_utf8(expr))
        if l:
            return True
        else:
            return False