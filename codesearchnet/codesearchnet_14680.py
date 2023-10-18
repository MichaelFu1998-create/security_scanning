def __set_baudrate(self, baud):
        """setting baudrate if supported"""
        log.info('Changing communication to %s baud', baud)
        self.__writeln(UART_SETUP.format(baud=baud))
        # Wait for the string to be sent before switching baud
        time.sleep(0.1)
        try:
            self._port.setBaudrate(baud)
        except AttributeError:
            #pySerial 2.7
            self._port.baudrate = baud