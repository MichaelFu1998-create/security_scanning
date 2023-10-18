def identity_is(self,item_category,item_type=None):
        """Check if the item described by `self` belongs to the given category
        and type.

        :Parameters:
            - `item_category`: the category name.
            - `item_type`: the type name. If `None` then only the category is
              checked.
        :Types:
            - `item_category`: `unicode`
            - `item_type`: `unicode`

        :return: `True` if `self` contains at least one <identity/> object with
            given type and category.
        :returntype: `bool`"""
        if not item_category:
            raise ValueError("bad category")
        if not item_type:
            type_expr=u""
        elif '"' not in item_type:
            type_expr=u' and @type="%s"' % (item_type,)
        elif "'" not in type:
            type_expr=u" and @type='%s'" % (item_type,)
        else:
            raise ValueError("Invalid type name")
        if '"' not in item_category:
            expr=u'd:identity[@category="%s"%s]' % (item_category,type_expr)
        elif "'" not in item_category:
            expr=u"d:identity[@category='%s'%s]" % (item_category,type_expr)
        else:
            raise ValueError("Invalid category name")

        l=self.xpath_ctxt.xpathEval(to_utf8(expr))
        if l:
            return True
        else:
            return False