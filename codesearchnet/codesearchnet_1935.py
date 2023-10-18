def arglist(self, args, call):
        """arglist: (argument ',')* (argument [','] |
                                     '*' test (',' argument)* [',' '**' test] |
                                     '**' test)"""
        for arg in args:
            if isinstance(arg, ast.keyword):
                call.keywords.append(arg)
            elif len(call.keywords) > 0:
                error = diagnostic.Diagnostic(
                    "fatal", "non-keyword arg after keyword arg", {},
                    arg.loc, [call.keywords[-1].loc])
                self.diagnostic_engine.process(error)
            else:
                call.args.append(arg)
        return call