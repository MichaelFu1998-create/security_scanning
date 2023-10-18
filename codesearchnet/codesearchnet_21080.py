def set_sleep(self, value=False):
        """Set device sleep timer."""
        return (yield from self.handle_set(self.API.get('sleep'), int(value)))