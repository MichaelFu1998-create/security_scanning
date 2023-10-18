def do_escape_nl(self, arg):
        """
        Escape newlines in any responses
        """
        if arg.lower() == 'off':
            self.escape_nl = False
        else:
            self.escape_nl = True