def stop(self):
        """Does cleanup of bot and plugins."""
        if self.webserver is not None:
            self.webserver.stop()
        if not self.test_mode:
            self.plugins.save_state()