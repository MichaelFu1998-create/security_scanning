def setup(self, port):
        """Connects to an Arduino UNO on serial port `port`.

        @throw RuntimeError can't connect to Arduino
        """
        port = str(port)
        # timeout is used by all I/O operations
        self._serial = serial.Serial(port, 115200, timeout=2)
        time.sleep(2)  # time to Arduino reset

        if not self._serial.is_open:
            raise RuntimeError('Could not connect to Arduino')

        self._serial.write(b'\x01')

        if self._serial.read() != b'\x06':
            raise RuntimeError('Could not connect to Arduino')

        ps = [p for p in self.available_pins() if p['digital']['output']]
        for pin in ps:
            self._set_pin_direction(pin['id'], ahio.Direction.Output)