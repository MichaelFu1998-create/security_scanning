def do_unfullscreen(self, widget):
        """
        Widget Action to set Windowed Mode.
        """
        self.unfullscreen()
        self.is_fullscreen = False
        self.bot._screen_ratio = None