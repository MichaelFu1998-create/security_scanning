def do_rewind(self, line):
        """
        rewind
        """
        self.print_response("Rewinding from frame %s to 0" % self.bot._frame)
        self.bot._frame = 0