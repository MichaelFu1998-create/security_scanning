def error(self, text):
        """SHOULD BE PRIVATE"""
        msg = 'Error with dev: {}, spi_speed: {} - {}'.format(
            self._dev, self._spi_speed, text)
        log.error(msg)
        raise IOError(msg)