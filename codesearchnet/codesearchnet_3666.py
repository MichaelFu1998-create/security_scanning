def is_declared(self, expression_var):
        """ True if expression_var is declared in this constraint set """
        if not isinstance(expression_var, Variable):
            raise ValueError(f'Expression must be a Variable (not a {type(expression_var)})')
        return any(expression_var is x for x in self.get_declared_variables())