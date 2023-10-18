def do_window_close(self, widget, data=None):
        """
        Widget Action to Close the window, triggering the quit event.
        """
        publish_event(QUIT_EVENT)

        if self.has_server:
            self.sock.close()

        self.hide_variables_window()

        self.destroy()
        self.window_open = False