def do_pause(self, line):
        """
        Toggle pause
        """
        # along with stuff in socketserver and shell
        if self.pause_speed is None:
            self.pause_speed = self.bot._speed
            self.bot._speed = 0
            self.print_response('Paused')
        else:
            self.bot._speed = self.pause_speed
            self.pause_speed = None
            self.print_response('Playing')