def run(self):
        """
        Receives the serial data into the self._raw buffer
        :return:
        """
        run_once = True
        while (run_once or self._threaded) and self.end is False:
            self.service_tx_queue()
            self.parse_messages()

            run_once = False

            if self._threaded:
                time.sleep(self._timeout)

        if self._threaded:
            logger.info('bootloader thread complete')