def run(self):
        """
        Wrapper function for TUN and serial port monitoring

        Wraps the necessary functions to loop over until self._isRunning
        threading.Event() is set(). This checks for data on the TUN/serial
        interfaces and then sends data over the appropriate interface. This
        function is automatically run when Threading.start() is called on the
        Monitor class.
        """
        while self.isRunning.is_set():
            try:
                try:
                    # self.checkTUN()
                    self.monitorTUN()

                except timeout_decorator.TimeoutError as error:
                    # No data received so just move on
                    pass
                self.checkSerial()
            except KeyboardInterrupt:
                break