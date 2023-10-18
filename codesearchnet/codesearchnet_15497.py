def swap(self, name):
        """ Swap variable name for variable value
        Args:
            name (str): Variable name
        Returns:
            Variable value (Mixed)
        """
        if name.startswith('@@'):
            var = self.variables(name[1:])
            if var is False:
                raise SyntaxError('Unknown variable %s' % name)
            name = '@' + utility.destring(var.value[0])
            var = self.variables(name)
            if var is False:
                raise SyntaxError('Unknown variable %s' % name)
        elif name.startswith('@{'):
            var = self.variables('@' + name[2:-1])
            if var is False:
                raise SyntaxError('Unknown escaped variable %s' % name)
            if isinstance(var.value[0], string_types):
                var.value[0] = utility.destring(var.value[0])
        else:
            var = self.variables(name)
            if var is False:
                raise SyntaxError('Unknown variable %s' % name)
        return var.value