def run(self):
        """
        Receives the serial data into the self._raw buffer
        :return:
        """
        run_once = True
        while run_once or self._threaded:
            waiting = self._port.in_waiting
            if waiting > 0:
                temp = [int(c) for c in self._port.read(waiting)]
                self._raw += temp

            self._parse_raw_data()
            run_once = False

            if self._threaded:
                time.sleep(self._timeout)