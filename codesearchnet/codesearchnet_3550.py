def _method(self, expression, *args):
        """
        Overload Visitor._method because we want to stop to iterate over the
        visit_ functions as soon as a valid visit_ function is found
        """
        assert expression.__class__.__mro__[-1] is object
        for cls in expression.__class__.__mro__:
            sort = cls.__name__
            methodname = 'visit_%s' % sort
            method = getattr(self, methodname, None)
            if method is not None:
                method(expression, *args)
                return
        return