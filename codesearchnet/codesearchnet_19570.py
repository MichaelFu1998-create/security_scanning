def update(self):
        """Update light objects to their current values."""
        bulbs = self._hub.get_lights()
        if not bulbs:
            _LOGGER.debug("%s is offline, send command failed", self._zid)
            self._online = False