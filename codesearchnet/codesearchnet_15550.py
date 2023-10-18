def with_units(self, val, ua, ub):
        """Return value with unit.
        args:
            val (mixed): result
            ua (str): 1st unit
            ub (str): 2nd unit
        raises:
            SyntaxError
        returns:
            str
        """
        if not val:
            return str(val)
        if ua or ub:
            if ua and ub:
                if ua == ub:
                    return str(val) + ua
                else:
                    # Nodejs version does not seem to mind mismatched
                    # units within expressions. So we choose the first
                    # as they do
                    # raise SyntaxError("Error in expression %s != %s" % (ua, ub))
                    return str(val) + ua
            elif ua:
                return str(val) + ua
            elif ub:
                return str(val) + ub
        return repr(val)