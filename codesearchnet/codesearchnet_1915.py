def exec_stmt(self, exec_loc, body, in_opt):
        """(2.6, 2.7) exec_stmt: 'exec' expr ['in' test [',' test]]"""
        in_loc, globals, locals = None, None, None
        loc = exec_loc.join(body.loc)
        if in_opt:
            in_loc, globals, locals = in_opt
            if locals:
                loc = loc.join(locals.loc)
            else:
                loc = loc.join(globals.loc)
        return ast.Exec(body=body, locals=locals, globals=globals,
                        loc=loc, keyword_loc=exec_loc, in_loc=in_loc)