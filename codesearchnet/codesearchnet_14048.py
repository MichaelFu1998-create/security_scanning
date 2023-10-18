def do_toggle_fullscreen(self, action):
        """
        Widget Action to Toggle fullscreen from the GUI
        """
        is_fullscreen = action.get_active()
        if is_fullscreen:
            self.fullscreen()
        else:
            self.unfullscreen()