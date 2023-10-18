def build(self, **kwargs):
        """Must be called before parse."""
        self.yacc = yacc.yacc(module=self, **kwargs)