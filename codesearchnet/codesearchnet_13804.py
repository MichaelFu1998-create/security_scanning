def do_play(self, line):
        """
        Resume playback if bot is paused
        """
        if self.pause_speed is None:
            self.bot._speed = self.pause_speed
            self.pause_speed = None
        self.print_response("Play")