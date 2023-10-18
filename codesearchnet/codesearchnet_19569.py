def set_all(self, red, green, blue, brightness):
        """Set color and brightness of bulb."""
        command = "C {},{},{},{},{},\r\n".format(self._zid, red, green, blue,
                                                 brightness)
        response = self._hub.send_command(command)
        _LOGGER.debug("Set all %s: %s", repr(command), response)
        return response