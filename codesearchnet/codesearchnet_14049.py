def do_toggle_play(self, action):
        """
        Widget Action to toggle play / pause.
        """
        # TODO - move this into bot controller
        # along with stuff in socketserver and shell
        if self.pause_speed is None and not action.get_active():
            self.pause_speed = self.bot._speed
            self.bot._speed = 0
        else:
            self.bot._speed = self.pause_speed
            self.pause_speed = None