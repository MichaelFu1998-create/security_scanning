def get_mute(self):
        """Check if the device is muted."""
        mute = (yield from self.handle_int(self.API.get('mute')))
        return bool(mute)