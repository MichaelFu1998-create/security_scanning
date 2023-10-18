def parse_args(self, args, scope):
        """Parse arguments to mixin. Add them to scope
        as variables. Sets upp special variable @arguments
        as well.
        args:
            args (list): arguments
            scope (Scope): current scope
        raises:
            SyntaxError
        """
        arguments = list(zip(args,
                             [' '] * len(args))) if args and args[0] else None
        zl = itertools.zip_longest if sys.version_info[
            0] == 3 else itertools.izip_longest
        if self.args:
            parsed = [
                v if hasattr(v, 'parse') else v for v in copy.copy(self.args)
            ]
            args = args if isinstance(args, list) else [args]
            vars = [
                self._parse_arg(var, arg, scope)
                for arg, var in zl([a for a in args], parsed)
            ]
            for var in vars:
                if var:
                    var.parse(scope)
            if not arguments:
                arguments = [v.value for v in vars if v]
        if not arguments:
            arguments = ''
        Variable(['@arguments', None, arguments]).parse(scope)