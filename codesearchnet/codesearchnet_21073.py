def set_mode(self, value):
        """Set the currently active mode on the device (DAB, FM, Spotify)."""
        mode = -1
        modes = yield from self.get_modes()
        for temp_mode in modes:
            if temp_mode['label'] == value:
                mode = temp_mode['band']

        return (yield from self.handle_set(self.API.get('mode'), mode))