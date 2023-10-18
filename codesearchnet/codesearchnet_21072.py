def get_mode(self):
        """Get the currently active mode on the device (DAB, FM, Spotify)."""
        mode = None
        int_mode = (yield from self.handle_long(self.API.get('mode')))
        modes = yield from self.get_modes()
        for temp_mode in modes:
            if temp_mode['band'] == int_mode:
                mode = temp_mode['label']

        return str(mode)