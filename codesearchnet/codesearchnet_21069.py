def set_power(self, value=False):
        """Power on or off the device."""
        power = (yield from self.handle_set(
            self.API.get('power'), int(value)))
        return bool(power)