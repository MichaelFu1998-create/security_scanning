def do_fullscreen(self, widget):
        """
        Widget Action to Make the window fullscreen and update the bot.
        """
        self.fullscreen()
        self.is_fullscreen = True
        # next lines seem to be needed for window switching really to
        # fullscreen mode before reading it's size values
        while Gtk.events_pending():
            Gtk.main_iteration()
        # we pass informations on full-screen size to bot
        self.bot._screen_width = Gdk.Screen.width()
        self.bot._screen_height = Gdk.Screen.height()
        self.bot._screen_ratio = self.bot._screen_width / self.bot._screen_height