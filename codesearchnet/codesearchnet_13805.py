def do_goto(self, line):
        """
        Go to specific frame
        :param line:
        :return:
        """
        self.print_response("Go to frame %s" % line)
        self.bot._frame = int(line)