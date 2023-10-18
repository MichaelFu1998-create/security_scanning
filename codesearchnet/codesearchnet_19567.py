def turn_on(self):
        """Turn bulb on (full brightness)."""
        command = "C {},,,,100,\r\n".format(self._zid)
        response = self._hub.send_command(command)
        _LOGGER.debug("Turn on %s: %s", repr(command), response)
        return response