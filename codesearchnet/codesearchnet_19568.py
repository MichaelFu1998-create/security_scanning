def set_brightness(self, brightness):
        """Set brightness of bulb."""
        command = "C {},,,,{},\r\n".format(self._zid, brightness)
        response = self._hub.send_command(command)
        _LOGGER.debug("Set brightness %s: %s", repr(command), response)
        return response