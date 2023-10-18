def handle_error(self, e, line, t='E'):
        """ Custom error handler
        args:
            e (Mixed): Exception or str
            line (int): line number
            t(str): Error type
        """
        self.register.register("%s: line: %d: %s\n" % (t, line, e))