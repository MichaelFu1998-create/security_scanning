def close(self):
        """
        This method will close the transport (serial port) and exit
        :return: No return value, but sys.exit(0) is called.
        """

        self._command_handler.system_reset()
        self._command_handler.stop()
        self.transport.stop()
        self.transport.close()

        if self.verbose:
            print("PyMata close(): Calling sys.exit(0): Hope to see you soon!")

        sys.exit(0)