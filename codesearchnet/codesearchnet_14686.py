def close(self):
        """restores the nodemcu to default baudrate and then closes the port"""
        try:
            if self.baud != self.start_baud:
                self.__set_baudrate(self.start_baud)
            self._port.flush()
            self.__clear_buffers()
        except serial.serialutil.SerialException:
            pass
        log.debug('closing port')
        self._port.close()