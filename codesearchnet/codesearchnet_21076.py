def set_mute(self, value=False):
        """Mute or unmute the device."""
        mute = (yield from self.handle_set(self.API.get('mute'), int(value)))
        return bool(mute)