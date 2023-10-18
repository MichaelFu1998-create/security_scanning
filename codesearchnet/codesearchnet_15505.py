def _parse_arg(self, var, arg, scope):
        """ Parse a single argument to mixin.
        args:
            var (Variable object): variable
            arg (mixed): argument
            scope (Scope object): current scope
        returns:
            Variable object or None
        """
        if isinstance(var, Variable):
            # kwarg
            if arg:
                if utility.is_variable(arg[0]):
                    tmp = scope.variables(arg[0])
                    if not tmp:
                        return None
                    val = tmp.value
                else:
                    val = arg
                var = Variable(var.tokens[:-1] + [val])
        else:
            # arg
            if utility.is_variable(var):
                if arg is None:
                    raise SyntaxError('Missing argument to mixin')
                elif utility.is_variable(arg[0]):
                    tmp = scope.variables(arg[0])
                    if not tmp:
                        return None
                    val = tmp.value
                else:
                    val = arg
                var = Variable([var, None, val])
            else:
                return None
        return var