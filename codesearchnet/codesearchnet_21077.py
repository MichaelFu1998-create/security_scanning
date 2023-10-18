def get_play_status(self):
        """Get the play status of the device."""
        status = yield from self.handle_int(self.API.get('status'))
        return self.PLAY_STATES.get(status)