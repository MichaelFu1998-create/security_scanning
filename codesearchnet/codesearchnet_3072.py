def emit(self, what, *args):
        ''' what can be either name of the op, or node, or a list of statements.'''
        if isinstance(what, basestring):
            return self.exe.emit(what, *args)
        elif isinstance(what, list):
            self._emit_statement_list(what)
        else:
            return getattr(self, what['type'])(**what)