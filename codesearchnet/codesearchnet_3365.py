def _assert(self, expression: Bool):
        """Auxiliary method to send an assert"""
        assert isinstance(expression, Bool)
        smtlib = translate_to_smtlib(expression)
        self._send('(assert %s)' % smtlib)