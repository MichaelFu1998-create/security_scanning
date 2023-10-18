def p_media_query_value(self, p):
        """ media_query_value           : number
                                        | variable
                                        | word
                                        | color
                                        | expression
        """
        if utility.is_variable(p[1]):
            var = self.scope.variables(''.join(p[1]))
            if var:
                value = var.value[0]
                if hasattr(value, 'parse'):
                    p[1] = value.parse(self.scope)
                else:
                    p[1] = value
        if isinstance(p[1], Expression):
            p[0] = p[1].parse(self.scope)
        else:
            p[0] = p[1]