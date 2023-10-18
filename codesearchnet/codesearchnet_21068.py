def get_power(self):
        """Check if the device is on."""
        power = (yield from self.handle_int(self.API.get('power')))
        return bool(power)