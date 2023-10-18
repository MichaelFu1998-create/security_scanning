def open(self, verbose):
        """
        open the serial port using the configuration data
        returns a reference to this instance
        """
        # open a serial port
        if verbose:
            print('\nOpening Arduino Serial port %s ' % self.port_id)

        try:

            # in case the port is already open, let's close it and then
            # reopen it
            self.arduino.close()
            time.sleep(1)
            self.arduino.open()
            time.sleep(1)
            return self.arduino

        except Exception:
            # opened failed - will report back to caller
            raise