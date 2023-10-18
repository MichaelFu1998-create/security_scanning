def assert_stmt(self, assert_loc, test, msg):
        """assert_stmt: 'assert' test [',' test]"""
        loc = assert_loc.join(test.loc)
        if msg:
            loc = loc.join(msg.loc)
        return ast.Assert(test=test, msg=msg,
                          loc=loc, keyword_loc=assert_loc)