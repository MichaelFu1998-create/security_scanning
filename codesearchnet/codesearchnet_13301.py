def xpath_eval(self,expr):
        """
        Evaluate XPath expression in context of `self.xmlnode`.

        :Parameters:
            - `expr`: the XPath expression
        :Types:
            - `expr`: `unicode`

        :return: the result of the expression evaluation.
        :returntype: list of `libxml2.xmlNode`
        """
        ctxt = common_doc.xpathNewContext()
        ctxt.setContextNode(self.xmlnode)
        ctxt.xpathRegisterNs("muc",self.ns.getContent())
        ret=ctxt.xpathEval(to_utf8(expr))
        ctxt.xpathFreeContext()
        return ret